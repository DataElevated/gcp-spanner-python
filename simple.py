#from typing import final
from ast import With
from tracemalloc import Snapshot
from typing import List
from google.cloud import spanner
from google.cloud.spanner_v1 import session
from google.oauth2 import service_account
from google.cloud import spanner_v1

TempMyCreds = service_account.Credentials.from_service_account_file('gcp.json')


# Instantiate Spanner Client
SpannerClient = spanner.Client(credentials=TempMyCreds)

InstanceID = 'production'
Instance = SpannerClient.instance(InstanceID)
Instance

DatabaseID = 'account'
Database = Instance.database(DatabaseID)
Database
Session = session.Session(DatabaseID)
print(Session)
#sys.exit(0)


def GetTopQueries():
    with Database.snapshot() as snapshot:
        Results = snapshot.execute_sql(
            'SELECT text,execution_count,avg_rows_scanned,interval_end FROM spanner_sys.query_stats_top_hour WHERE interval_end = (SELECT MAX(interval_end) FROM spanner_sys.query_stats_top_hour) ORDER BY avg_rows_scanned DESC'
        )

        finalOutput = f'Results from top Queries: \n'
        for row in Results:
            finalOutput += 'Interval End: {}\n'.format(row[3])
            finalOutput += 'SQL: {}\n'.format(row[0])
            finalOutput += 'Execution Count: {}\n'.format(row[1])
            finalOutput += 'Average Rows Scanned: {}\n'.format(row[2])
            finalOutput += f'\n'
        
        """ for row in Results:
            print('Interval End: {}'.format(row[3]))
            print('SQL: {}'.format(row[0]))
            print('Execution Count: {}'.format(row[1]))
            print('Average Rows Scanned: {}'.format(row[2]))
            print('')
         """
        return(finalOutput)

def GetFailedTransactions():
    with Database.snapshot() as snapshot:
        Results = snapshot.execute_sql(
            """
            SELECT text, request_tag,interval_end,execution_count,all_failed_execution_count,all_failed_avg_latency_seconds,avg_latency_seconds,avg_rows,avg_bytes,avg_rows_scanned,avg_cpu_seconds 
                FROM spanner_sys.query_stats_top_hour
                WHERE all_failed_execution_count > 0 
                ORDER BY interval_end DESC
            """
        )


        print('Results from Failed Queries:')
        for row in Results:
            print('SQL: {}'.format(row[0]))
            print('request_tag: {}'.format(row[1]))
            print('interval_end: {}'.format(row[2]))
            print('execution_count: {}'.format(row[3]))
            print('all_failed_execution_count: {}'.format(row[4]))
            print('all_failed_avg_latency_seconds: {}'.format(row[5]))
            print('avg_latency_seconds: {}'.format(row[6]))
            print('avg_rows: {}'.format(row[7]))
            print('avg_bytes: {}'.format(row[8]))
            print('avg_rows_scanned: {}'.format(row[9]))
            print('avg_cpu_seconds: {}'.format(row[10]))

def GetFailedTransactionsCount():
    with Database.snapshot() as snapshot:
        Results = snapshot.execute_sql(
            """
            SELECT interval_end,all_failed_execution_count
            FROM spanner_sys.query_stats_total_hour
            WHERE interval_end = "2022-04-21T01:00:00Z" 
            ORDER BY interval_end;
            """
        )

        for row in Results:
            print('{} - Failed Count: {} '.format(row[0], row[1]))

def UpdateInstance():
    Instance.reload()
    config = Instance.node_count
    print(f'{config} and {config}\n')
    Instance.node_count = 3
    Operation = Instance.update()
    Results = Operation.result()
    print(Results)

def GetInstanceNodes():
    Instance.reload()
    Results = Instance.node_count
    print(Results)

# [START spanner_list_databases]
def ListSpannerDatabases(instance_id, database_id, SpannerClient):
    """Lists databases and their leader options."""
    #TempMyCreds = service_account.Credentials.from_service_account_file('gcp.json')
    spanner_client = SpannerClient
    instance = spanner_client.instance(instance_id)
    
    databases = list(instance.list_databases())
    for MyDatabase in databases:
        print(MyDatabase.name)
        return(MyDatabase.name)
# [END spanner_list_databases]

def DeleteSpannerSessions(MyDb, MyCreds):
    # Create a client
    #TempMyCreds = service_account.Credentials.from_service_account_file('gcp.json')
    client = spanner_v1.SpannerClient(credentials=MyCreds)

    # Initialize request argument(s)
    request = spanner_v1.ListSessionsRequest(
        database=MyDb,
    )

    # Make the request
    page_result = client.list_sessions(request=request)

    # Handle the response
    for response in page_result:
        print('Deleting: {}'.format(response.name))
        delrequest = spanner_v1.DeleteSessionRequest(
            name=response.name,
            )
        client.delete_session(request=delrequest)

if __name__ == '__main__':
    #Result = GetTopQueries()
    #print(Result)
    #GetInstanceNodes()
    MyDatabaseID = ListSpannerDatabases('production', 'account', SpannerClient=SpannerClient)
    DeleteSpannerSessions(MyDatabaseID, MyCreds=TempMyCreds)
    #GetFailedTransactions()
    #GetFailedTransactionsCount()