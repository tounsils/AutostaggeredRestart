# AutostaggeredRestart


Restarting the ArcGIS Server services

The challenge is how it will be scheduled so that all machines are not restarted at the same time. What we may have to do is combine SSM with Lambda. Basically what you would have to do is something like this

Restart Portal 1

Health check portal 1 , wait till ready

Restart Portal 2

Health check portal 2, wait till ready

Count number of instances of ArcGIS Server on Autoscaling Group and store the instances in an array

Repeat the following for the array

Restart instanceN

Healthcheck instanceN wait til ready

Restart datastore 1

Health check datastore 1, wait till ready

Restart datastore 2

Health check datastore 2,wait till ready

RESTART PROCESSING COMPLETE
