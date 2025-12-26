from loadcsvtopostgres import testmethod
import os
print( os.getcwd() )

def main():
    # Load data from CSV to PostgreSQL
    # data = pd.read_csv('data/data.csv')
    # data.to_sql('data', con=engine, if_exists='replace', index=False)
    testmethod()
    
if __name__ == '__main__':
    main()