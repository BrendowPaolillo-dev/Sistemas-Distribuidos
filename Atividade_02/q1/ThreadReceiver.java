import java.io.*;
import java.net.*;
// import java.util.*;

/*
    Sistema de chat via UDP
    Desenvolvedores: Brendow e Lucas

    Classe:     ThreadReceiver

    Execução:   javac ThreadReceiver.java


    Funcionamento:  Recebe a mensagem do cliente para o outro;
                    Imprime na tela;

*/

public class ThreadReceiver extends Thread {
    DatagramSocket dgramSocket = null;
    //método construtor
    public ThreadReceiver(DatagramSocket dgramSocket) {
        try {
            this.dgramSocket = dgramSocket;
        } catch (Exception e) {
            // TODO: handle exception
        }
    }
    
    //execução principal
    @Override
    public void run() {
        try {

            while (true) {
                // cria um buffer para receber requisições
                byte[] buffer = new byte[1000]; 

                // cria um pacote vazio
                DatagramPacket dgramPacket = new DatagramPacket(buffer, buffer.length);
                // aguarda a chegada de datagramas
                this.dgramSocket.receive(dgramPacket);

                byte[] received = dgramPacket.getData();
                
                //tamanho do nome na posição 0 do vetor
                byte nickSize = received[0];
                
                //pega a parte do nome em bytes e converte para uma String
                byte[] nickByte = new byte[nickSize];
                System.arraycopy(received, 1, nickByte, 0, nickSize);
                String nick = new String(nickByte);

                //pega o tamanho da mensagem
                byte msgSize = received[1+nickSize];
                //pega a mensagem e converte para uma String
                byte[] msgByte = new byte[msgSize];
                System.arraycopy(received, 2 + nickSize, msgByte, 0, msgSize );
                String msg = new String(msgByte);

                //imprime o nome do usuário e a resposta
                System.out.println("Resposta do " + nick + ": " + msg );

            } // while
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } finally {
            this.dgramSocket.close();
        }
    }
}