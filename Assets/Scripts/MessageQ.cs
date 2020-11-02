using System;
using System.Net;
using System.Threading;
using System.Text;
using System.Collections;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Security.Cryptography;
using UnityEngine;

namespace SQ
{
    public class SQEle
    {
        public byte[] data {get;set;}
        public delegate void SendCallBack();
        public SendCallBack callBack {get;set;}
        public Socket sock {get;set;}

        public void ServiceCallBack()
        {
            this.callBack();
        }
    }

    public class SendQ
    {
        public Queue Q;
        public ManualResetEvent EnqEvent {get;}
        public void Enq(SQEle ele)
        {
            this.Q.Enqueue(ele);
            this.EnqEvent.Set();
        }

        public SQEle next()
        {
            var ret  = (SQEle)this.Q.Dequeue();
            if(this.Q.Count==0)
            {
                this.EnqEvent.Reset();
            }
            return ret;
        }

        public void QStopMsg()
        {
            this.Q.Enqueue("STOP");
            this.EnqEvent.Set();
        }
    }

}

