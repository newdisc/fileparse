package com.newdisc.sms;

import javax.xml.bind.annotation.XmlType;
/**
 * 
/home/srikanth/dev/dwld/calls.xsl
/home/srikanth/dev/dwld/calls-20180418091036.xml
/home/srikanth/dev/dwld/sms.xsl
/home/srikanth/dev/dwld/sms-20180418091036.xml
<smses count="7997" backup_set="3435c98e-aae6-4c41-a9c3-746445b653b0" 
backup_date="1524022839378">
  <sms protocol="0" address="DMAmazon" date="1457752021332" 
  type="1" subject="null" 
  body="Arriving Today: Your package with Voltas 185JY Split AC (1.5 Ton, 5 Star Rating, Whi~ will be delivered by AmzAgent(7030902522). Track http://amzn.in/7tCaoyM" 
  toa="null" sc_toa="null" service_center="+919768399176" read="1" status="-1" 
  locked="0" date_sent="1457752018000" readable_date="12 Mar 2016 8:37:01 a.m." 
  contact_name="(Unknown)" />

 * 
 */

@XmlType(name = "sms")
public class SMS {
    public String address;
    public String date;
    public String subject;
    public String body;
    public String service_center;
    public String contact_name;
    private String original;
    public String getOriginal(){
        return original;
    }
    public void setOriginal(final String org) {
        original = org;
    }
}