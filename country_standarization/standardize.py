import re
from typing import Union
from warnings import warn

import pandas as pd

from country_standarization.data.countries_pattern import default_countries_pattern
from country_standarization.data.iso_3166 import iso_3166


def correct_names(df: Union[pd.Series, pd.DataFrame], column: str, pattern_map: str = None,
                  new_colum_name: str = None) -> Union[pd.DataFrame, pd.Series]:
    """
    Standardize names of countries according to ISO 3166.
    :param standardize_names:
    :param pattern_map: list of tuple maping between names and regex
    :param df: dataframe with countries
    :param column: column name where countries are
    :param new_colum_name: If you want to give a new name to sio country names.
    :return: A dataframe with a column with iso names of the countries.
    """

    # Find individual names
    def find_country_name(country_name: str, pattern_list: list, verbose: bool = True) -> str:
        for name, pattern in pattern_list:
            if len(pattern.findall(country_name)) > 0:
                return name

        # We could not find a match
        if verbose:
            warn(f"Warning: country {country_name} not found. Using given name")
        return country_name

    if pattern_map is None:
        pattern_map = default_countries_pattern

    # Compile patterns
    countries_pattern = [(name, re.compile(patt, re.IGNORECASE)) for name, patt in pattern_map]

    names_countries = df[column].to_list()

    names_countries = [find_country_name(name, pattern_list=countries_pattern, verbose=True) for name in
                       names_countries]

    df = df.copy()
    if new_colum_name is None:
        df[column] = names_countries
        return df
    else:
        df[new_colum_name] = names_countries
        return df


def map_names(df: Union[pd.Series, pd.DataFrame], column_to_match: str, on: str, extra_columns: str,
              standardize_names: bool = True) -> Union[
    pd.DataFrame, pd.Series]:
    """
    Returns extrac columns with information on the iso codes for countries.
    :param df: Dataframe to change match
    :param column_to_match: name of the on the df to match
    :param on: name of iso options to match ['name', 'alpha-2', 'alpha-3', 'country-code', 'iso_3166-2']
    :param extra_columns: If we should return more columns options are:
        ['name', 'alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'region',
        'sub-region', 'intermediate-region', 'region-code', 'sub-region-code',
        'intermediate-region-code']
    :return:
    """

    if not isinstance(extra_columns, list):
        extra_columns = [extra_columns]

    if on not in ['name', 'alpha-2', 'alpha-3', 'country-code', 'iso_3166-2']:
        raise KeyError(f"on is {on} and should be in: ['name', 'alpha-2', 'alpha-3', 'country-code', 'iso_3166-2']")

    for col in extra_columns:
        valid_cols = ['name', 'alpha-2', 'alpha-3', 'country-code', 'iso_3166-2', 'region',
                      'sub-region', 'intermediate-region', 'region-code', 'sub-region-code',
                      'intermediate-region-code']
        if col not in valid_cols:
            raise KeyError(f"extra_columns must be in {valid_cols}, {col} is not.")

    # get dataFrames to merge
    iso_df = pd.DataFrame(iso_3166)
    df = df.copy()

    if standardize_names:
        df[column_to_match] = correct_names(df, column=column_to_match)[column_to_match]

    columns = extra_columns
    iso_filtered = iso_df[["name"] + columns]
    iso_filtered = iso_filtered.rename(columns={on: column_to_match})

    # Merge
    return pd.merge(df, iso_filtered, how="left", on=column_to_match)
