package com.newdisc;

import java.io.File;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import com.newdisc.sms.SMS;
import com.newdisc.sms.SMSList;

/**
 * Hello world!
 *
 */
public class App 
{
    final static String[] nointSend = {
            "FPANDA", "MVINSY", "MISETS"
        };
    final static String[] intSend = {
            "HDFCBK", "SBI", "INDUS"
            //"HDFCBK", "SBI", "INDUS"
            //, "DMMSWIPE", "IPAYTM", "YOUBRO", "MSILDL", 
            //"VMOLAMNY"
        };
    public static boolean addrOfIntr(String addr, String[] interest) {
        List<String> matchpat = Arrays.stream(interest).filter(
            pat -> addr.contains(pat)
        )
        .collect(Collectors.toList());
        return !matchpat.isEmpty();
    }
    public static void main( String[] args )
    {    
        final String[] asend = {"VKHDFCBK", "DMMSWIPE", "RMHDFCBK", 
            "DZHDFCBK", "DMHDFCBK", "DM-HDFCBK", "VM-IPAYTM", "VK-IPAYTM",
            "VMOLAMNY", "DMYOUBRO", "VK-MSILDL", "VK-YOUBRO", "MM-HDFCBK", "AM-YOUBRO"
        };
        //"VMOLAMNY", "DMYOUBRO", "VK-MSILDL", "VK-YOUBRO", "MM-HDFCBK", "AM-YOUBRO",
        //DMAmazon
        final Set<String> intSenders = new HashSet<>(Arrays.asList(asend));
        Stream.of(args).forEach(System.out::println);
        try {
            File file = new File(args[0]);
            JAXBContext jaxbContext = JAXBContext.newInstance(SMSList.class);
            Unmarshaller jaxbUnmarshaller = jaxbContext.createUnmarshaller();
            final SMSList smslst = (SMSList) jaxbUnmarshaller.unmarshal(file);
            System.out.println("List of SMSes of length : " + smslst.smses.size());
            //System.out.println(smslst.smses);
            final List<SMS> smses = smslst.smses;
            final List<SMS> amzsms = smses.stream().
                //filter(sms -> ! intSenders.contains(sms.address)).
                //filter(sms -> ! addrOfIntr(sms.address)).
                filter(sms -> addrOfIntr(sms.address, intSend)).
                //filter(sms -> ! addrOfIntr(sms.address, nointSend)).
                //filter(sms -> sms.body.matches(".*pay.*")).
                collect(Collectors.toList());
            //forEach(System.out::println);
            System.out.println("Interest List of SMSes of length : " + amzsms.size());
            System.out.println(amzsms);
         } catch (JAXBException e) {
            e.printStackTrace();
          }
    }
}
