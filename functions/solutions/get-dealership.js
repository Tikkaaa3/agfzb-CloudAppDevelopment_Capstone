const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.postAllDocs({db: 'dealerships',includeDocs: true,
       limit: 10});
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
      
      const service = CloudantV1.newInstance({});

}
