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
  public String response = String.Empty;
}

public class ProcessPipeline
{
  public SendQ sendQ = new SendQ();
  public RecvQ recvQ = new RecvQ();
  public Socket S;
  public bool Running;

  public void StartPipeLine()
  {
    try
    {
      IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Loopback, 5003);
      S = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
      Debug.Log("begin connect");
      S.BeginConnect(localEndPoint, new AsyncCallback(ConnectCallback), null);
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
      S.EndConnect(ar);
      Debug.Log("connected");
      SQEle.sock = S;
      StartSendThread();
      StartRecvThread(S);
    }
    catch (Exception e)
    {
      Console.WriteLine(e.ToString());
    }
  }

  private void StartSendThread()
  {
    byte[] byteData = SQEle.ConvertToBytes("started send thread");
    SQEle msg = new SQEle(byteData, testcallback);
    sendQ.Enq(msg);
    SQEle msg_ = sendQ.next();
    SQEle.sock.BeginSend(msg_.data, 0, msg_.data.Length, 0, new AsyncCallback(SendCallBack), msg_);
  }

  private void SendCallBack(IAsyncResult ar)
  {
    SQEle msg = (SQEle)ar.AsyncState;
    SQEle.sock.EndSend(ar);
    Debug.Log("sent");
    msg.ServiceCallBack();
    sendQ.EnqEvent.WaitOne();
    var next_msg = sendQ.next();
    if (next_msg.Equals("STOP"))
    {
      return;
    }
    else
    {
      SQEle.sock.BeginSend(next_msg.data, 0, next_msg.data.Length, 0, new AsyncCallback(SendCallBack), next_msg);
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

  public void StartRecvThread(Socket client)
  {
    try
    {
      StateObject state = new StateObject();
      state.workSocket = client;
      Debug.Log("begin recieve");
      client.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);
    }
    catch (Exception e)
    {
      Console.WriteLine(e.ToString());
    }
  }

  public void ReceiveCallback(IAsyncResult ar)
  {
    StateObject state = (StateObject)ar.AsyncState;
    int bytesread = state.workSocket.EndReceive(ar);
    if (bytesread > 0)
    {
      state.response = state.response + Encoding.ASCII.GetString(state.buffer, 0, bytesread);
      int EOM_idx = state.response.IndexOf("END_OF_MSG");
      while (EOM_idx > 0)
      {
        recvQ.Enq(state.response.Substring(0, EOM_idx));
        state.response = state.response.Substring(EOM_idx + 10);
        EOM_idx = state.response.IndexOf("END_OF_MSG");
      }
      state.workSocket.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);
    }
  }

  public System.Collections.Generic.IEnumerable<String> RecvAll()
  {
    String ret;
    while (true)
    {
      ret = recvQ.next();
      if (ret == String.Empty)
      {
        break;
      }
      else
      {
        yield return ret;
      }
    }
  }
}
