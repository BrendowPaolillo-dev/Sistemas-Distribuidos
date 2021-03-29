import java.io.*;
import java.util.*;
import java.net.*;

/**
 * UDPClient: Cliente UDP Descricao: Envia uma msg em um datagrama e recebe a
 * mesma msg do servidor
 */


public class UDPClient {
    

    public static void main(String args[]) {
        
        Scanner reader = new Scanner(System.in);
        
        System.out.println("Digite seu nome: ");
        String nick = reader.nextLine();
        try {
            DatagramSocket dgramSocket = new DatagramSocket(6666);
            byte[] nickBytes = new byte[] {(byte) nick.getBytes("UTF-8").length};

            ThreadSender ts = new ThreadSender(nick, nickBytes, dgramSocket);
            ThreadReceiver tr = new ThreadReceiver(dgramSocket);
    
            ts.start();
            tr.start();

        } catch (Exception e) {
            //TODO: handle exception
        }



    } //main	
}
