package com.newdisc.sms;

import java.util.List;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlRootElement(name = "smses")
@XmlType
public class SMSList {
    @XmlElement(name="sms")
    public List<SMS> smses;
    public SMSList(){
        System.out.println("Creating SMSList");
    }
}
