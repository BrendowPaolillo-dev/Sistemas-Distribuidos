import java.io.*;
import java.util.*;
import java.net.*;

/*
    Sistema de chat via UDP
    Desenvolvedores: Brendow e Lucas

    Classe:     Cliente

    Execução:   javac UDPClient.java
                java UDPClient
                Digite o IP do cliente

    Funcionamento:  O programa conecta o cliente ao cliente;
                    Envia o nome do cliente para o outro;
                    Cria uma thread de recebimento de mensagens e envio;

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
