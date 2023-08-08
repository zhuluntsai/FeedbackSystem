using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.IO.Ports;
using System.Threading;

public class GetDistance : MonoBehaviour
{
    public string Port = "/dev/cu.usbmodem144201";
    public int BaudRate = 115200;
    public double MinFrequency = 10;
    public double MaxFrequency = 100;
    public double MinDistance = 0;
    public double MaxDistance = 3;
    public int DelayTime = 50; // ms
    string LogPath = "StimLog.txt";
    string log = "";    

    double slopeA;
    double constantB; 
    double stimFreq;
    SerialPort sp;

    public GameObject Cube1;
    public GameObject Cube2;
    public float Distance;

    void FrequencyGenerate(double distance)
    {
        // Calculate the frequency according to the distance
        stimFreq = 0.0;
        if (distance >= MinDistance && distance <= MaxDistance)
        {
            stimFreq = slopeA * distance + constantB;
        }
        else if (distance < MinDistance || distance > MaxDistance)
        {
            stimFreq = 0.0;
        }
        
        // Export the frequency to the log and the stimulator
        stimFreq = System.Math.Round(stimFreq, 2);
        distance = System.Math.Round(distance, 2);
        string line = "Frequency: " + stimFreq + ", Distance: " + distance;
        Debug.Log(line);
        log += System.DateTime.Now.ToString("yyyy/MM/dd HH:mm:ss.ff") + ", " + line + "\n";
        try
        {
            sp.Write(stimFreq.ToString());
        }
        catch (System.Exception e)
        {
            Debug.Log(e.Message);
        }
    }
    
    void Start()
    {
        Debug.Log("start");

        // Check the port of the stimulator
        try
        {
            sp = new SerialPort(Port, BaudRate);
            sp.Open();
        }
        catch (System.Exception e)
        {
            Debug.Log(e.Message);
        }

        // Calculate the slope of the frequency
        slopeA = (MaxFrequency-MinFrequency) / (MinDistance-MaxDistance);
        constantB = 0.5 * ((MaxFrequency+MinFrequency) - slopeA * (MinDistance+MaxDistance));

        // Export the parameter to the log
        log += "Port: " + Port + "\n";
        log += "BaudRate: " + BaudRate + "\n";
        log += "MinFrequency: " + MinFrequency + "\n";
        log += "MaxFrequency: " + MaxFrequency + "\n";
        log += "MinDistance: " + MinDistance + "\n";
        log += "MaxDistance: " + MaxDistance + "\n";
        log += "DelayTime: " + DelayTime + "\n";
    }

    void Update()
    {
        Distance = Vector3.Distance(Cube1.transform.position, Cube2.transform.position);
        
        FrequencyGenerate(Distance);
        Thread.Sleep(DelayTime);
    }

    void OnDestroy()
    {
        Debug.Log("Log exported on " + LogPath);
        
        // Close the stimulator
        try
        {
            sp.Write("0.0");
        }
        catch (System.Exception e)
        {
            Debug.Log(e.Message);
        }

        // Write the log
        using (StreamWriter writer = new StreamWriter(LogPath))
        {
            writer.WriteLine(log);
        }
    }
}
