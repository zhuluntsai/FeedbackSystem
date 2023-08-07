using System;
using System.IO.Ports;
using System.Threading;
using UnityEngine;
using System.IO.Ports;
using System.Threading;

namespace StimGeneratorApp
{
    class StimGenerator
    {
        private string port = "COM9";
        private int baudRate = 115200;
        private double minFreq = 10;
        private double maxFreq = 100;
        private double minDis = 10;
        private double maxDis = 100;
        private int delayFlag = 0;
        private double timeStart = 0.0;
        private double timeCurrent = 0.0;
        private double delayDesired = 0.05;

        private double slopeA;
        private double constantB;

        public static SerialPort sp = new SerialPort(port, baudRate);

        public StimGenerator()
        {
            // Initialize your parameters here if needed
        }

        public void OpenConnection()
    {
        if (sp!=null)
        {
            if(sp.IsOpen)
            {
                sp.Close();
                print("Closing port, because it's already open");
            }
            else
            {
                sp.Open();
                sp.ReadTimeout = 100;
                print("port open");
            }
        }
        else 
        {
            if(sp.IsOpen)
            {
                print("port is already open");
            }
            else{
                print("port == null");
            }
        }
        
    } 

        public void ParameterSetting(double minFrequency, double maxFrequency, double minDistance, double maxDistance, int limitValue)
        {
            if (limitValue == 1)
            {
                minFreq = minFrequency;
            }
            else if (limitValue == 0)
            {
                minFreq = 0;
            }

            maxFreq = maxFrequency;
            minDis = minDistance;
            maxDis = maxDistance;

            slopeA = (maxFreq - minFreq) / (minDis - maxDis);
            constantB = 0.5 * ((maxFreq + minFreq) - slopeA * (minDis + maxDis));
        }

        private void DelayFunc(double delayTime)
        {
            DateTime start = DateTime.Now;
            while ((DateTime.Now - start).TotalSeconds <= delayTime)
            {
                // Do nothing, just wait
            }
        }

        private double FreqGenerator(int mode, double dis)
        {
            double stimFreqVal = 0.0;
            if (mode == 10)
            {
                if (dis >= minDis && dis <= maxDis)
                {
                    stimFreqVal = slopeA * dis + constantB;
                }
                else if (dis > maxDis)
                {
                    stimFreqVal = 0.0;
                }
                else if (dis < minDis)
                {
                    stimFreqVal = 0.0;
                }
            }
            else if (mode == 20)
            {
                if (dis > 100)
                {
                    stimFreqVal = 100;
                }
                else if (dis < 0)
                {
                    stimFreqVal = 0;
                }
                else
                {
                    stimFreqVal = dis;
                }
            }

            Console.WriteLine(stimFreqVal);
            return stimFreqVal;
        }

        public void StimGenerate(int comStatus, int mode, int sync, double dis, double tempInput)
        {
            double freq = 0.0;

            if (comStatus == 0)
            {
                // Implement your code for comStatus == 0
            }
            else if (comStatus == 1)
            {
                freq = 0.0;
                // Implement your code for comStatus == 1
            }
            else if (comStatus == 2)
            {
                // Implement your code for comStatus == 2
            }
            else if (comStatus == 3)
            {
                // Implement your code for comStatus == 3
            }
        }

        static void Main(string[] args)
        {
            StimGenerator stimGenerator = new StimGenerator();
            // Call your methods here to test
        }
    }
}
