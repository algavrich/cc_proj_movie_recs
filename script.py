"""Codecademy CS career path recommendation software portfolio project."""

import pandas as pd
import unicodedata
from collections import defaultdict
from random import sample
from typing import List


def create_movie_dict() -> defaultdict:
    """Create dictionary of release years mapped to list of movie titles."""

    movie_data = pd.read_csv('movie_metadata.csv', header=0)
    movie_data = movie_data.dropna(subset=['title_year'])
    movie_data = movie_data.reset_index()

    movie_dict = defaultdict(list)

    for i in range(len(movie_data)):
        year = movie_data['title_year'][i]
        title = unicodedata.normalize(
            'NFKD',
            movie_data['movie_title'][i],
        ).strip()
        movie_dict[str(round(year))].append(title)

    return movie_dict


def sort_years(movie_dict: defaultdict) -> List[str]:
    """Create sorted list of release years for easy search."""

    return sorted(movie_dict.keys())


def get_possible_years(
        movie_dict: defaultdict,
        sorted_years: List[str],
        input_str: str,
    ) -> List[str]:
    """Get list of possible release years from user input of year string."""

    input_len = len(input_str)

    if input_len == 4:
        if input_str not in movie_dict:
            return []
        
        return [input_str]
    
    else:
        possible_years = []
        for i in range(len(sorted_years)):
            if sorted_years[i][:input_len] == input_str:
                curr_idx = i
                while (curr_idx < len(sorted_years)
                       and sorted_years[curr_idx][:input_len] == input_str):
                    possible_years.append(sorted_years[curr_idx])
                    curr_idx += 1
                break

        return possible_years


def display_movies(movie_dict: defaultdict, year: str) -> None:
    """Print list of movies for a given year."""

    movies = movie_dict[year]
    if len(movies) > 10:
        movies = sample(movies, 10)

    for movie in movies:
        print(movie)


def recommend(movie_dict: defaultdict) -> None:
    """Perform recommendations from user input."""

    print('Welcome to Movie Recommendations by Release Year')

    rec = True

    while rec:
        input_str = input(
            'Type the beginning of the year you would like to see: '
        )
        if len(input_str) > 4:
            print('Year must be 4 digits or less')
            continue

        else:
            possible_years = get_possible_years(
                movie_dict,
                sort_years(movie_dict),
                input_str,
            )

            if not possible_years:
                print(''.join([
                    'We don\'t have any recommendations ',
                    'for that year, please try another',
                ]))
                continue

            elif len(possible_years) == 1:
                if len(input_str) < 4:
                    print(''.join([
                        'There is one year in our system that matches your ',
                        'request: ',
                        possible_years[0],
                    ]))
                    is_desired = input(
                        'Would you like to see movies for this year? [y/n]: '
                    ).lower()

                    if is_desired != 'y':
                        continue

                print(''.join([
                    'Here are some movies that were released in ',
                    possible_years[0],
                ]))
                display_movies(movie_dict, possible_years[0])

                see_more = input(
                    'Would you like to search for a different year? [y/n]: '
                ).lower()
                if see_more != 'y':
                    break

            else:
                print('Here are some years that match your request:\n')
                print(possible_years)

    print('Thank you for using Movie Recommendations by Release Year')

            
def main() -> None:
    """Create movie dictionary and invoke recommendation function."""

    recommend(create_movie_dict())


main()
