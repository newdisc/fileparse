package com.newdisc.sms;

import java.util.List;

import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlRootElement(name = "smses")
@XmlType(name = "smses")
public class SMSList {
    public List<SMS> smses;
}
