package com.newdisc;

import java.io.File;
import java.util.stream.Stream;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import com.newdisc.sms.SMSList;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        Stream.of(args).forEach(System.out::println);
        try {
            File file = new File(args[0]);
            JAXBContext jaxbContext = JAXBContext.newInstance(SMSList.class);
            Unmarshaller jaxbUnmarshaller = jaxbContext.createUnmarshaller();
            final SMSList smslst = (SMSList) jaxbUnmarshaller.unmarshal(file);
            System.out.println(smslst.smses);
         } catch (JAXBException e) {
            e.printStackTrace();
          }
    }
}
