# Authors: Sergio Stinchi

# Version        Description
# 1.0.0          Starting version

# Import
import sys
import glob
from string import replace


commonPath = info.getCommonPath() 
resourcesPath = info.getResourcesPath()
execfile("%s/%s" % (commonPath, "Utility.py"))
execfile("%s/%s" % (commonPath, "LogLevelSetting.py"))


# Auxiliary functions
def reset(text, arg):
   if len(text) > 0: log.INFO(text)
   if AdminConfig.hasChanges() == 1: AdminConfig.reset()
   log.INFO( "Execute on file %s done" % arg)
   return -1

# Auxiliary functions
def clearExit(text, status):
   if len(text): log.INFO( text)
   AdminConfig.reset()
   log.INFO( "%s done" % scriptName)
   sys.exit(status)
   return
# Variables
scriptName = "createDatasource.py"
version = "1.5.3"
log.setClass(scriptName)

# Command Line
argc = len(sys.argv)
if argc < 1: 
   log.INFO( "Usage: %s {<target data file pattern>}+" % (scriptName))
   sys.exit(-1)
        
# Start
log.INFO( "%s V%s" % (scriptName, version))

defagedTimeout = "0"                         
defpurgePolicy = "EntirePool"                
defreapTime = "180"                          
defunusedTimeout = "1800"                    
defconnectionTimeout = "180"                 
defmaxConnections = 10                       
defminConnections = 1                        
defstatementCacheSize = "100"                


# Target data file loop
savecount = 0
for filepattern in sys.argv:
   log.INFO( "Execute on file pattern %s ..." % filepattern)
   filenames = glob.glob(filepattern)
   for arg in filenames:
      log.INFO( "Execute on file %s ..." % arg)

      # Data
      scopeName = ''                            # mandatory [The name of the resource scope (i.e: Telematico, DogTelProNode01, ...) ]
                                                #            Warning: if the scope is a server and its name is not unique on the cell 
                                                #                     it must be used the form <Node>:<Server> 
      name = ''                                 # mandatory [The name of the Data Source]     
      jndiName = ''                             # mandatory [The jndi of the Data Source]
      dataStoreHelperClassName = ''             # mandatory [The name of the DataStoreHelper implementation class, 
                                                #            i.e: com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper, com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper and so on]
      providerName = ''                         # mandatory [The configuration object Id of the JDBC provider to which the new data source will belong]
      configurationParameters = []              # optional  [A list of all the required resources: name, type, value
                                                #            i.e.: [ ['URL', 'java.lang.String', 'jdbc:oracle:thin:@26.2.163.221:1521:A10A'] ] ]
      optConfigurationParameters = []           # optional  [A list of some not required resources, i.e.: [ ['traceLevel', 'java.lang.Integer', '-1'] ] ]
      description = ''                          # optional  [A description of the Data Source]
      category = ''                             # optional  [Data Source category]
      containerManagedPersistence = 'false'     # optional  [Specifies if the data source is used also for container managed persistence for enterprise beans
                                                #            Admitted values: true or false]
      # Authentication Alias data
      authenticationAlias = ''                  # optional  [Authentication Alias Name used for database authentication at run time
                                                #            If this attribute, authenticationUsername and authenticationPassword are all inserted the script will also create the alias if not existing]
      authenticationUsername = ''               # optional  [Authentication Alias Username]
      authenticationPassword = ''               # optional  [Authentication Alias Password]
      authenticationDescription = ''            # optional  [Authentication Alias Description]
      xaRecoveryAuthAlias = ''                  # optional  [XA Recovery Authentication Alias]
      containerManagedAlias = ''                # optional  [Container Authentication Alias]
      mappingConfigAlias=''                     # optional  [mapping onfig Alias]
      # Connection Pool data 
      agedTimeout = defagedTimeout              # optional  [Specifies the interval in seconds before a physical connection is discarded.
                                                #            DefaultValue=0]
      purgePolicy = defpurgePolicy              # optional  [Specifies how to purge connections when a stale connection or fatal connection error is detected. 
                                                #            Admitted values: EntirePool or FailingConnectionOnly. DefaultValue=EntirePool]
      reapTime = defreapTime                    # optional  [Specifies the interval, in seconds, between runs of the pool maintenance thread.
                                                #            DefaultValue=180]
      unusedTimeout = defunusedTimeout          # optional  [Specifies the interval in seconds after which an unused or idle connection is discarded.
                                                #            DefaultValue=1800]
      connectionTimeout = defconnectionTimeout  # optional  [Specifies the interval, in seconds, after which a connection request times out and a ConnectionWaitTimeoutException is thrown.
                                                #            DefaultValue=180]
      maxConnections = defmaxConnections        # optional  [Maximum number of connections for the pool. 
                                                #            DefaultValue=10]
      minConnections = defminConnections        # optional  [Minimum number of connections for the pool. 
                                                #            DefaultValue=1]
      # Other data
      statementCacheSize=defstatementCacheSize  # optional  [The number of cachable statements per connection. A value of 0 disables statement pooling
                                                #            DefaultValue=100]
      authMechanismPreference=''                # optional  [Specifies the authentication mechanism. Valid values are BASIC_PASSWORD for basic authentication and KERBEROS for Kerberos authentication
                                                #            Admitted values: BASIC_PASSWORD and KERBEROS]
      deleteIfExist = 0                         # 1 = delete the resource if exists

      
      # Read target data file
      log.INFO( "Read target data file ...")
      try: execfile(arg)
      except IOError, ioe:
         log.ERROR(str(ioe))
         sys.exit(-1)
      else: log.INFO( "Read target data file done")

      # Check data read
      log.INFO( "Check data read ...")

      if (scopeName == None) or (len(scopeName.strip()) == 0):
         log.ERROR("The variable scopeName is mandatory") 
         log.INFO( "%s done" % (scriptName) ) 
         sys.exit(-1) 

      if (name == None) or (len(name.strip()) == 0):
         log.ERROR("The variable name is mandatory")
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if (jndiName == None) or len(jndiName.strip()) == 0:
         log.ERROR("The variable jndiName is mandatory")
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if (dataStoreHelperClassName == None) or len(dataStoreHelperClassName.strip()) == 0:
         log.ERROR("The variable dataStoreHelperClassName is mandatory")
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if (providerName == None) or len(providerName.strip()) == 0:
         log.ERROR("The variable providerName is mandatory")
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if len(configurationParameters) > 0:
         if isinstance(configurationParameters, type([])) == 0:
            log.ERROR("The variable configurationParameters must be a list")
            log.INFO( "%s done" % (scriptName)) 
            sys.exit(-1)

         for dummy in configurationParameters:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               log.ERROR("Each object of variable configurationParameters must be a list of three items")
               log.INFO( "%s done" % (scriptName)) 
               sys.exit(-1)

      if len(optConfigurationParameters) > 0:
         if isinstance(optConfigurationParameters, type([])) == 0:
            log.ERROR("The variable optConfigurationParameters must be a list")
            log.INFO( "%s done" % (scriptName)) 
            sys.exit(-1)

         for dummy in optConfigurationParameters:
            if isinstance(dummy, type([])) == 0 or len(dummy) != 3:
               log.ERROR("Each object of variable optConfigurationParameters must be a list of three items")
               log.INFO( "%s done" % (scriptName)) 
               sys.exit(-1)

      if containerManagedPersistence.strip() not in ['true', 'false']:
         log.ERROR("The variable containerManagedPersistence is boolean")
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if (agedTimeout == None) or len(agedTimeout.strip()) == 0 :
         log.INFO( "WARNING: The variable agedTimeout has to be >= 0. Using default %s" % (defagedTimeout)) 
         agedTimeout = defagedTimeout
      else:
         if agedTimeout.strip().isdigit():
            if int(agedTimeout) <0:
               log.INFO( "WARNING: The variable agedTimeout has to be >= 0. Using default %s" % (defagedTimeout)) 
               agedTimeout = defagedTimeout
         else:
            log.INFO( "WARNING: The variable agedTimeout has to be numeric. Using default %s" % (defagedTimeout)) 
            agedTimeout = defagedTimeout

      if (purgePolicy == None) or len(purgePolicy.strip()) == 0 :
         log.INFO( "WARNING: The variable purgePolicy has to be EntirePool or FailingConnectionOnly. Using default %s" % (defpurgePolicy)) 
         purgePolicy = defpurgePolicy
      else:
         if purgePolicy.strip() not in ['EntirePool', 'FailingConnectionOnly']:
            log.INFO( "WARNING: The variable purgePolicy has to be EntirePool or FailingConnectionOnly. Using default %s" % (defpurgePolicy)) 
            purgePolicy = defpurgePolicy

      if (reapTime == None) or len(reapTime.strip()) == 0 :
         log.INFO( "WARNING: The variable reapTime has to be >= 0. Using default %s" % (defreapTime)) 
         reapTime = defreapTime
      else:
         if reapTime.strip().isdigit():
            if int(reapTime) <0:
               log.INFO( "WARNING: The variable reapTime has to be >= 0. Using default %s" % (defreapTime)) 
               reapTime = defreapTime
         else:
            log.INFO( "WARNING: The variable reapTime has to be numeric. Using default %s" % (defreapTime)) 
            reapTime = defreapTime

      if (unusedTimeout == None) or len(unusedTimeout.strip()) == 0 :
         log.INFO( "WARNING: The variable unusedTimeout has to be >= 0. Using default %s" % (defunusedTimeout)) 
         unusedTimeout = defunusedTimeout
      else:
         if unusedTimeout.strip().isdigit():
            if int(unusedTimeout) <0:
               log.INFO( "WARNING: The variable unusedTimeout has to be >= 0. Using default %s" % (defunusedTimeout)) 
               unusedTimeout = defunusedTimeout
         else:
            log.INFO( "WARNING: The variable unusedTimeout has to be numeric. Using default %s" % (defunusedTimeout)) 
            unusedTimeout = defunusedTimeout

      if (connectionTimeout == None) or len(connectionTimeout.strip()) == 0 :
         log.INFO( "WARNING: The variable connectionTimeout has to be >= 0. Using default %s" % (defconnectionTimeout)) 
         connectionTimeout = defconnectionTimeout
      else:
         if connectionTimeout.strip().isdigit():
            if int(connectionTimeout) <0:
               log.INFO( "WARNING: The variable connectionTimeout has to be >= 0. Using default %s" % (defconnectionTimeout)) 
               connectionTimeout = defconnectionTimeout
         else:
            log.INFO( "WARNING: The variable connectionTimeout has to be numeric. Using default %s" % (defconnectionTimeout)) 
            connectionTimeout = defconnectionTimeout

      if (maxConnections == None) or len(maxConnections.strip()) == 0 :
         log.INFO( "WARNING: The variable maxConnections has to be >= 0. Using default %s" % (defmaxConnections)) 
         maxConnections = defmaxConnections
      else:
         if maxConnections.strip().isdigit():
            if int(maxConnections) <0:
               log.INFO( "WARNING: The variable maxConnections has to be >= 0. Using default %s" % (defmaxConnections)) 
               maxConnections = defmaxConnections
         else:
            log.INFO( "WARNING: The variable maxConnections has to be numeric. Using default %s" % (defmaxConnections)) 
            maxConnections = defmaxConnections

      if (minConnections == None) or len(minConnections.strip()) == 0 :
         log.INFO( "WARNING: The variable minConnections has to be >= 0. Using default %s" % (defminConnections)) 
         minConnections = defminConnections
      else:
         if minConnections.strip().isdigit():
            if int(minConnections) <0:
               log.INFO( "WARNING: The variable minConnections has to be >= 0. Using default %s" % (defminConnections)) 
               minConnections = defminConnections
         else:
            log.INFO( "WARNING: The variable minConnections has to be numeric. Using default %s" % (defminConnections)) 
            minConnections = defminConnections

      if (statementCacheSize == None) or len(statementCacheSize.strip()) == 0 :
         log.INFO( "WARNING: The variable statementCacheSize has to be >= 0. Using default %s" % (defstatementCacheSize)) 
         statementCacheSize = defstatementCacheSize
      else:
         if statementCacheSize.strip().isdigit():
            if int(statementCacheSize) <0:
               log.INFO( "WARNING: The variable statementCacheSize has to be >= 0. Using default %s" % (defstatementCacheSize)) 
               statementCacheSize = defstatementCacheSize
         else:
            log.INFO( "WARNING: The variable statementCacheSize has to be numeric. Using default %s" % (defstatementCacheSize)) 
            statementCacheSize = defstatementCacheSize

      if (authMechanismPreference != None) and len(authMechanismPreference.strip()) != 0 :
         if authMechanismPreference.strip() not in ['BASIC_PASSWORD', 'KERBEROS']:
            log.INFO( "ERROR: The variable authMechanismPreference has to be BASIC_PASSWORD or KERBEROS") 
            log.INFO( "%s done" % (scriptName)) 
            sys.exit(-1)

      if minConnections > maxConnections:
         log.INFO( "ERROR: The variable minConnections must be lesser or equal to variable maxConnections") 
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)

      if deleteIfExist not in [0, 1]:
         log.INFO( "ERROR: The variable deleteIfExist can be 0 or 1") 
         log.INFO( "%s done" % (scriptName)) 
         sys.exit(-1)
         
      log.INFO( "Check data read done") 

      # Check scopeName ...
      log.INFO( "Check scope %s ..." % (scopeName)) 
      (scope , scopeid, scopeName, nodeName, serverName, clusterName) = checkScopeName(scopeName)
     
      # Create Datasource
      log.INFO( "Create Datasource ... for provider %s " %(providerName)) 
      scopeRes = getStringScopeForId(scope, scopeid, scopeName, nodeName, serverName, clusterName)
      log.INFO( "ScopeRes = %s   for providerName %s " %(scopeRes,providerName)) 
      provider = AdminConfig.getid(scopeRes + '/JDBCProvider:' + providerName + '/')
      if len(provider) == 0:
         log.INFO( "ERROR: The JDBC Provider %s doesn't exist for the given scope" % (providerName)) 
         clearExit("Rollback and exit", -1)
      datasource = AdminConfig.getid(scopeRes + '/JDBCProvider:' + providerName + '/DataSource:' + name)
      if len(datasource) > 0:
         log.INFO( "Datasource %s already exists" % name) 
         if deleteIfExist == 1:
            log.INFO( "Delete existing Datasource:",1) 
            try:
               AdminConfig.remove(datasource)
               log.INFO( "OK",2) 
            except: 
               reset("KO\nRollback and exit", arg)
               continue
         else: continue

      try:
         if len(authenticationAlias.strip()) > 0 and len(authenticationUsername.strip()) > 0 and len(authenticationPassword.strip()) > 0:
            found = 0
            jaasAliasStr = AdminConfig.list('JAASAuthData')
            if len(jaasAliasStr)>0:
               jaasAliasList = jaasAliasStr.split(lineSeparator)
               for jaasAlias in jaasAliasList:
                  if authenticationAlias == AdminConfig.showAttribute(jaasAlias, 'alias'):
                     log.INFO( "Autentication Alias %s already exist" %(authenticationAlias)) 
                     found = 1
                     break
            else:
                found = 0
            if found == 0:
               log.INFO( "Create Authentication Alias %s:" % (authenticationAlias),1) 
               security = AdminConfig.getid('/Cell:' + AdminControl.getCell() + '/Security:/')
               alias = ['alias', authenticationAlias]
               userid = ['userId', authenticationUsername]
               password = ['password', authenticationPassword]      
               if len(authenticationDescription.strip()) > 0: jaasAttrs = [alias, userid, password, ['description', authenticationDescription]]
               else: jaasAttrs = [alias, userid, password]
               AdminConfig.create('JAASAuthData', security, jaasAttrs)
               log.INFO( "OK",2) 
            else:
               log.INFO( "Authentication Alias %s already exists" % (authenticationAlias)) 
                
         log.INFO( "Create %s:" % (name),1) 
         command = "[-name '" + name + "' -jndiName '" + jndiName + "' -dataStoreHelperClassName " + dataStoreHelperClassName
         if len(configurationParameters) > 0:
            command += " -configureResourceProperties ["
            for parameter in configurationParameters:
               if (parameter[2] != None) and len(parameter[2].strip()) != 0:
                  command += "['" + parameter[0] + "' '" + parameter[1] + "' '" + parameter[2] + "']"
            command += "]"
         #log.INFO( "command = %s" % (command)
         if len(description.strip()) > 0: command += " -description '" + description + "'"
         if len(category.strip()) > 0: command += " -category '" + category + "'"
         if len(authenticationAlias.strip()) > 0: command += " -componentManagedAuthenticationAlias '" + authenticationAlias + "'"
         if len(xaRecoveryAuthAlias.strip()) > 0: command += " -xaRecoveryAuthAlias '" + xaRecoveryAuthAlias + "'"
         command += " -containerManagedPersistence " + containerManagedPersistence + "]"  
         datasource = AdminTask.createDatasource(provider, command)
         log.INFO("OK",2)
         connectionPool = AdminConfig.showAttribute(datasource, 'connectionPool')
         log.INFO("Modify ConnectionPoolParams",1)
         ConnectionPoolParams = "['agedTimeout'  '" + str(agedTimeout) + "'] ['purgePolicy' '" + str(purgePolicy) + "'] ['reapTime' '" + str(reapTime) + "'] ['unusedTimeout' '" + str(unusedTimeout) + "'] ['connectionTimeout' '" + str(connectionTimeout) + "'] ['maxConnections' '" + str(maxConnections) + "'] ['minConnections' '" + str(minConnections) + "']"
         AdminConfig.modify(connectionPool, '[' + str(ConnectionPoolParams) + ']')
         log.INFO( " OK",2)
         if len(statementCacheSize) > 0:
            log.INFO( "Modify statementCacheSize",1)
            AdminConfig.modify(datasource, [['statementCacheSize', statementCacheSize]])
            log.INFO( " OK",2)
         if len(authMechanismPreference.strip()) > 0:
            log.INFO( "Modify authMechanismPreference",1)
            AdminConfig.modify(datasource, [['authMechanismPreference ', authMechanismPreference]])
            log.INFO( " OK",2)
         log.INFO( "Define resourceProperties",1)
         propertySet = AdminConfig.showAttribute(datasource, 'propertySet')
         resourceProperties = AdminConfig.showAttribute(propertySet, 'resourceProperties')[1:-1].split()
         for parameter in optConfigurationParameters:
            log.INFO("Parameter to add or modified %s" %(parameter))
            modified = 0
            for property in resourceProperties:            
               search = property[0:property.find('(')]         
               if parameter[0] == search: 
                  log.INFO( " property %s already present , proceed to modify" %(parameter[0]))
                  AdminConfig.modify(property, "[['value' '" + parameter[2] + "']]")
                  modified = 1
            if modified == 0:
               attr = [['name', parameter[0]], ['value', parameter[2]], ['type', parameter[1]], ['required', 'false']]
               AdminConfig.create('J2EEResourceProperty', propertySet, attr)      
         log.INFO( " OK",2)
         log.INFO("create Mapping Module",1)
         if containerManagedAlias!='None' and containerManagedAlias!='':
            if mappingConfigAlias=='': mappingConfigAlias='DefaultPrincipalMapping'
            map_att_1 = ['authDataAlias',containerManagedAlias]
            map_att_2 = ['mappingConfigAlias',mappingConfigAlias]
            mapAttrs = [map_att_1, map_att_2]
            AdminConfig.create('MappingModule', datasource, mapAttrs)
         log.INFO( " OK",2)
      except:
         log.INFO( " KO",2)
         type, value, traceback = sys.exc_info()
         log.ERROR( "%s (%s)" % (str(value), type))
         reset("Rollback and exit", arg)
         continue
      log.INFO( "Create Datasource done")
      if AdminConfig.hasChanges() == 1:
         # Save
         log.INFO( "Save ...") 
         AdminConfig.save()
         savecount += 1
         log.INFO( "Save done") 
      
      log.INFO( "Execute on file %s done" % arg ) 
   log.INFO( "Execute on file pattern %s done" % filepattern) 

if savecount > 0:
   # Synchronization 
   log.INFO( "Synchronization ...") 
   nodes = AdminControl.queryNames('type=NodeSync,*')
   if len(nodes) > 0:
      nodelist = nodes.split(lineSeparator)      
      for node in nodelist:
         beg = node.find('node=') + 5
         end = node.find(',', beg)
         log.INFO( "Synchronization for node \"" + node[beg:end] + "\" :",1) 
         try: AdminControl.invoke(node, 'sync')
         except: log.INFO("KO",2) 
         else: log.INFO( "OK",2) 
   else:
      log.INFO( "No running nodeagents found") 
log.INFO( "Synchronization done") 

# Done
log.INFO( "%s V%s done" % (scriptName, version)) 
