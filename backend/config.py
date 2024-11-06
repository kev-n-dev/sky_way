local_envars = {
    'db-user': "skyway",
    'db-name': "skyway",
    'db-password': "skyway",
    'db-host':"rds",
}
def envar_exists(key):
    return key in local_envars

def get(key):
    if envar_exists(key):
        envar = local_envars.get(key, None)
        return envar
    else:
        return None


 