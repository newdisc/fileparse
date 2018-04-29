package com.newdisc.sms;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;
/**
 * 
/dev/dwld/calls.xsl
/dev/dwld/calls-20180418091036.xml
/dev/dwld/sms.xsl
/dev/dwld/sms-20180418091036.xml
<smses count="7997" backup_set="3435c98e-aae6-4c41-a9c3-746445b653b0" 
backup_date="1524022839378">
  <sms protocol="0" address="DMAmazon" date="1457752021332" 
  type="1" subject="null" 
  body="Arriving Today" 
  toa="null" sc_toa="null" service_center="+919768399176" read="1" status="-1" 
  locked="0" date_sent="1457752018000" readable_date="12 Mar 2016 8:37:01 a.m." 
  contact_name="(Unknown)" />

 * 
 */

@XmlType(name = "sms")
public class SMS {
    @XmlAttribute
    public String address;
    public String date;
    @XmlAttribute
    public String subject;
    @XmlAttribute
    public String body;
    @XmlAttribute
    public String service_center;
    public String contact_name;
    private String original;
    public String getOriginal(){
        return original;
    }
    public void setOriginal(final String org) {
        original = org;
    }
    public String toString() {
        final String[] cols = {address, body, "\n"};
        //{address, subject, body, service_center, "\n"};
        final String tst = Stream.of(cols).collect(Collectors.joining("|"));
        final List cls = Arrays.asList(cols);
        return String.join("|", cls);
    }
}