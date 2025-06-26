# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed


//gcp
30 1,5,9,12,18,23 * * * root export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_bill_stat daily >> /workspace/logs/crontab 2>&1

0 6,11,13,16,22 * * * root export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_bill_stat latest >> /workspace/logs/crontab 2>&1

0 2 * * * root export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_bill_stat monthly >> /workspace/logs/crontab 2>&1

15 4,12,20 * * * root export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_billing_sync daily >> /workspace/logs/crontab 2>&1

15 6,11,13,16,22 * * * root export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_billing_sync latest >> /workspace/logs/crontab 2>&1

//aws


5 */12 * * * root /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync daily >> /workspace/logs/crontab 2>&1

0 3 * * * root /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync monthly >> /workspace/logs/crontab 2>&1

7 23 2,3 * * root /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync daily last >> /workspace/logs/crontab 2>&1

7 23 2,3 * * root /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync monthly last >> /workspace/logs/crontab 2>&1

11 23 * * * root /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.bill_alarm.gcp_alarm monthly >> /workspace/logs/crontab 2>&1

#clean aws billing files
2 10 * * 4  root /workspace/project/wingyouth/bill_sync_script/apps/clean_file/clean_aws_file.sh


  989  /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync daily >> /workspace/logs/crontab 2>&1
  990  /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync daily 20250301-20250401>> /workspace/logs/crontab 2>&1
  995  /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync monthly 202503 >> /workspace/logs/crontab 2>&1
  996  /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.aws_billing_sync monthly 20250401-20250501 >> /workspace/logs/crontab 2>&1


export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_billing_sync daily 20250331 >> /workspace/logs/crontab 2>&1
export https_proxy="socks5://127.0.0.1:1080" && /root/anaconda3/condabin/conda run -n base python /workspace/project/wingyouth/bill_sync_script/index.py apps.cur_collector.gcp_bill_stat daily  20250402 >> /workspace/logs/crontab 2>&1
