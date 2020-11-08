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
        public byte[] data;
        public delegate void SendCallBack();
        public SendCallBack callBack;
        public static Socket sock;

        public SQEle(byte[] data,SendCallBack callBack)
        {
            this.data = data;
            this.callBack = callBack;
        }
        public void ServiceCallBack()
        {
            callBack();
        }
    }

    public class SendQ
    {
        public Queue Q;
        public ManualResetEvent EnqEvent = new ManualResetEvent(false);

        public SendQ()
        {
            Q = new Queue();
        }

        public void Enq(SQEle ele)
        {
            Q.Enqueue(ele);
            EnqEvent.Set();
        }

        public SQEle next()
        {
            var ret  = (SQEle)Q.Dequeue();
            if(Q.Count==0)
            {
                EnqEvent.Reset();
            }
            return ret;
        }

        public void QStopMsg()
        {
            Q.Enqueue("STOP");
            EnqEvent.Set();
        }
    }

    public class RecvQ
    {
        public Queue Q;
        public ManualResetEvent IsEmpty = new ManualResetEvent(false);

        public RecvQ()
        {
            Q = new Queue();
        }

        public void Enq(String recv_text)
        {
            Q.Enqueue(recv_text);
            IsEmpty.Reset();
        }

        public String next()
        {   String ret = String.Empty;
            if(Q.Count>0)
            {
                ret  = (String)Q.Dequeue();
            }
            if(Q.Count==0)
            {
                IsEmpty.Reset();
            }
            return ret;
        }

        public void QStopMsg()
        {
            // how to stop recv thread
        }        
    }

}

