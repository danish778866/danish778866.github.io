import pandas as pd

def block_candidates(candidate_set, table_A, table_B, output_file):
    A = pd.read_csv(table_A)
    B = pd.read_csv(table_B)
    CS = pd.read_csv(candidate_set)
    A.columns = ['A_id', 'id', 'name', 'year', 'duration', 'genre', 'actors', 'Up_System']
    B.columns = ['B_id', 'id', 'name', 'year', 'duration', 'genre', 'actors', 'Up_System']
    m1 = pd.merge(CS, A, on='A_id')
    m2 = pd.merge(m1, B, on='B_id')
    m3 = m2.loc[m2['year_x'] == m2['year_y']]
    m4 = m3[['A_id', 'B_id']]
    m4.to_csv(output_file, index=False)

def main():
    table_A = "imdb_table"
    table_B = "tmdb_table"
    candidate_set = "candidate_set"
    block_candidates(candidate_set, table_A, table_B, "blocked_candidate_set.csv")

if __name__ == "__main__":
    main()
