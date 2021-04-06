import java.io.*;
import java.net.*;

public class UDPServer {
    public static void main(String args[]){
        try {
            // cria um socket datagrama em uma porta especifica
            DatagramSocket dgramSocket = new DatagramSocket(6666);
            try {
               
                while (true) {
                   byte[] buffer = new byte[1024]; // cria um buffer para receber requisições
    
                   /* cria um pacote vazio */
                   DatagramPacket dgramPacket = new DatagramPacket(buffer, buffer.length);
                   dgramSocket.receive(dgramPacket); // aguarda a chegada de datagramas
    
                   byte[] fileNameBytes = dgramPacket.getData();
                   
                //    byte nickSize = received[0];
                   
                //    byte[] nickByte = new byte[nickSize];
                //    System.arraycopy(received, 1, nickByte, 0, nickSize);
                   String fileName = new String(fileNameBytes);
    
                //    byte msgSize = received[1+nickSize];
                //    byte[] msgByte = new byte[msgSize];
                //    System.arraycopy(received, 2 + nickSize, msgByte, 0, msgSize );
                //    String msg = new String(msgByte);
    
                   System.out.println("Nome do arquivo: " + fileName);
    
               } // while
           } catch (SocketException e) {
               System.out.println("Socket: " + e.getMessage());
           } catch (IOException e) {
               System.out.println("IO: " + e.getMessage());
           } finally {
               dgramSocket.close();
           }
        } catch (Exception e) {
            //TODO: handle exception
        }
    }
}
