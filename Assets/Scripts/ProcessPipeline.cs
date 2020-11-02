using System;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Collections;
using SQ;
using UnityEngine;
using UnityEngine.UI;


public class StateObject
{
    public Socket workSocket = null;
    public const int BufferSize = 1024;
    public byte[] buffer = new byte[BufferSize];
}

public class ProcessPipeline
{
    public SendQ sendQ = new SendQ();
    public Socket S;
    public bool Running; 
    public void StartPipeLine()
    {
        try
        {
            IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
            IPAddress ipAddr = ipHost.AddressList[0];
            IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 11111);
            S = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
            S.BeginConnect(localEndPoint, new AsyncCallback(ConnectCallback), S);
        }
        catch (Exception e)
        {
            Console.WriteLine(e.ToString());
        }
    }

    private void ConnectCallback(IAsyncResult ar)
    {
        try
        {  
            Socket S_ = (Socket)ar.AsyncState;
            S_.EndConnect(ar);
            Debug.Log("connected");
            StartSendThread();
        }
        catch (Exception e)
        {
            Console.WriteLine(e.ToString());
        }
    }

    private void StartSendThread()
    {   
        byte[] byteData = Encoding.ASCII.GetBytes("Started Send Thread");
        SQEle msg = new SQEle(){data=byteData,callBack=testcallback,sock=S};
        sendQ.Enq(msg);
        SQEle msg_ = sendQ.next();
        msg_.sock.BeginSend(msg_.data,0,msg_.data.Length,0,new AsyncCallback(SendCallBack),msg_);
    }

    private void SendCallBack(IAsyncResult ar)
    {
        SQEle msg = (SQEle) ar.AsyncState;
        msg.sock.EndSend(ar);
        msg.ServiceCallBack();
        sendQ.EnqEvent.WaitOne();
        var next_msg = sendQ.next();
        if(next_msg.Equals("STOP"))
        {
            return;
        }
        else
        {
            next_msg.sock.BeginSend(next_msg.data,0,next_msg.data.Length,0,new AsyncCallback(SendCallBack),next_msg);
        }
    }

    private void testcallback()
    {
        Debug.Log("test call back executed");
    }

    public void EndSendThread()
    {
        sendQ.QStopMsg();
    }

}
