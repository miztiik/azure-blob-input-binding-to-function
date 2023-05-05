param deploymentParams object
param storageQueueParams object
param saName string

// Get reference of SA
resource r_sa 'Microsoft.Storage/storageAccounts@2021-06-01' existing = {
  name: saName
}


resource r_qSvcs 'Microsoft.Storage/storageAccounts/queueServices@2021-04-01' = {
  name: 'default'
  parent: r_sa
  properties: {
    }
  }

resource r_storage_q 'Microsoft.Storage/storageAccounts/queueServices/queues@2022-09-01' = {
  parent: r_qSvcs
  name: '${storageQueueParams.queueNamePrefix}-q-${deploymentParams.global_uniqueness}'
  properties: {
    metadata: {}
  }
}

output queueName string = r_storage_q.name
output queueId string = r_storage_q.id
