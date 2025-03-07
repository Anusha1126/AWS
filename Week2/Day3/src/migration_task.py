import boto3
import json
import time

# Initialize AWS DMS client
dms_client = boto3.client('dms')

# Define DMS Task Configuration
replication_task_id = "mysql-postgre-migration"
source_endpoint_arn = "arn:aws:dms:us-east-1:970547378939:endpoint:RUI3AT4FYVB4VGCYQARFWVSOQE"
target_endpoint_arn = "arn:aws:dms:us-east-1:970547378939:endpoint:WCQKVFOVPBASLDG5ZNFIQF352I"
replication_instance_arn = "arn:aws:dms:us-east-1:970547378939:rep:EWPF27MXSFBCLP7CCBWMGFEL5U"

# Define Table Mappings (Proper JSON Format)
table_mappings_dict = {
    "rules": [
        {
            "rule-type": "selection",
            "rule-id": "1",
            "rule-name": "IncludeAllTables",
            "rule-action": "include",
            "object-locator": {
                "schema-name": "mydatabase",
                "table-name": "%"
            }
        }
    ]
}

# Convert to JSON String
table_mappings = json.dumps(table_mappings_dict)

try:
    # Create a DMS Replication Task
    response = dms_client.create_replication_task(
        ReplicationTaskIdentifier=replication_task_id,
        SourceEndpointArn=source_endpoint_arn,
        TargetEndpointArn=target_endpoint_arn,
        MigrationType="full-load",  # Moves all existing data
        TableMappings=table_mappings,
        ReplicationInstanceArn=replication_instance_arn
    )

    # Get Task ARN
    task_arn = response["ReplicationTask"]["ReplicationTaskArn"]
    print(f"DMS Replication Task '{replication_task_id}' has been created successfully.")
    print(f"Task ARN: {task_arn}")

    # Wait for the task to reach 'ready' state before starting
    while True:
        task_status = dms_client.describe_replication_tasks(
            Filters=[{"Name": "replication-task-arn", "Values": [task_arn]}]
        )["ReplicationTasks"][0]["Status"]

        print(f"Waiting for task to be ready. Current status: {task_status}")

        if task_status in ["ready"]:
            break  # Task is ready to start

        elif task_status in ["creating"]:
            time.sleep(10)  # Wait and check again

        else:
            raise Exception(f"Task cannot be started. Current Status: {task_status}")

    # Start the Replication Task
    dms_client.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType="start-replication"
    )

    print(f"Replication Task '{replication_task_id}' has started successfully.")

except Exception as e:
    print(f"Error: {str(e)}")