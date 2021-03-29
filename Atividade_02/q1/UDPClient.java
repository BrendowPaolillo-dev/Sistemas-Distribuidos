import java.io.*;
import java.util.*;

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
            byte[] nickBytes = new byte[] {(byte) nick.getBytes("UTF-8").length};
            System.out.println(nickBytes);

            ThreadSender ts = new ThreadSender(nick, nickBytes);
            ThreadReceiver tr = new ThreadReceiver();
    
            ts.start();
            tr.start();

        } catch (Exception e) {
            //TODO: handle exception
        }



    } //main	
}
