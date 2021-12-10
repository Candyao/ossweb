#!/bin/bash
function stop_sts()
{
   pid=`ps -ef | grep GetSts | grep -v grep | awk '{print $2}'`
   echo $pid
   kill $pid
}
case $1 in
stop)
  stop_sts
  ;;
  
start)
  gunicorn -b 127.0.0.1:8800 GetSts:sts_app --daemon --error-logfile gunicorn.log --access-logfile gunicorn.access.log --capture-output
  ;;

*)
  echo "error"
;;
esac
