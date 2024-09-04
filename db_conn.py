import ibm_db as db
 
class DbConn:
    
    def __init__(self):
        self.DATABASE = "bludb"
        self.HOSTNAME = "55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
        self.PORT = "31929"
        self.SECURITY = "SSL"
        self.CERTIFICATE = "DigiCertGlobalRootCA.crt"
        self.USR_ID = "gsn72184"
        self.PWD = "ZRf94OLTEXMofGfz"

        self.dsn =(
                "DATABASE={0};"
                "HOSTNAME={1};"
                "PORT={2};"
                "SECURITY={3};"
                "SSLServerCertificate={4};"
                "UID={5};"
                "PWD={6};"
        ).format(self.DATABASE,self.HOSTNAME,self.PORT,self.SECURITY,self.CERTIFICATE,self.USR_ID,self.PWD)

    def connect(self):

        dsn = self.dsn
        try:
            conn = db.connect(dsn,"","")
            print("Connection Successfull")
            return conn

        except:

            print("Unable to connect:",db.conn_errormsg())
