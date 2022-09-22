using System;
using System.Net;
using System.Net.Sockets;
using System.Net.NetworkInformation;
using System.Text;

namespace PingTraceRoute
{
    class PingRouteTracer
    {
        private const int MaxHops = 20;
        private const AddressFamily Family = AddressFamily.InterNetwork;
        private const int Timeout = 120;

        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                System.Console.WriteLine("[!!] No host specified");
                string appName = System.AppDomain.CurrentDomain.FriendlyName;
                System.Console.WriteLine("usage: {0} <host>", appName);
                System.Console.WriteLine("example: {0} google.com", appName);
                return;
            }

            string endHost = args[0];
            IPAddress endHostIP = null;
            IPHostEntry endHostEntry;

            try
            {
                endHostEntry = Dns.GetHostEntry(endHost);
            }
            catch (SocketException ex)
            {
                System.Console.WriteLine(ex.Message);
                return;
            }

            foreach (var ip in endHostEntry.AddressList)
            {
                if (ip.AddressFamily == Family)
                {
                    endHostIP = ip;
                }
            }

            if (endHostIP == null)
            {
                System.Console.WriteLine("[!!] Cannot find IPv4 address of host");
                return;
            }

            System.Console.WriteLine("Trace for host {0} ({1}):", endHost, endHostIP.ToString());

            using (var pinger = new Ping())
            {
                PingOptions opts = new PingOptions();
                opts.DontFragment = true;

                string data = "deez nuts";
                byte[] buffer = System.Text.Encoding.ASCII.GetBytes(data);
                
                for (int i = 1; i <= MaxHops; i++)
                {
                    try 
                    {
                        opts.Ttl = i;

                        PingReply reply = pinger.Send(endHostIP.ToString(), Timeout, buffer, opts);

                        System.Console.WriteLine("{0} -> {1}", i, reply.Address.ToString());

                        if (reply.Address.Equals(endHostIP))
                        {
                            return;
                        }
                    }
                    catch
                    {
                        System.Console.WriteLine("{0} -> *", i);
                        continue;
                    }
                }
            }
        }
    }
}