import java.io.*;
import java.net.*;
import java.util.*;

/*
    Sistema de chat via UDP
    Desenvolvedores: Brendow e Lucas

    Classe:     ThreadSender

    Execução:   javac ThreadSender.java


    Funcionamento:  O programa conecta o cliente ao cliente;
                    Envia a mensagem do cliente para o outro;
                    Organiza os dados dos pacotes a serem enviados;

*/

public class ThreadSender extends Thread {
    DatagramSocket dgramSocket;
    String resp;
    String nick;
    byte[] nickBytes;

    //método construtor
    public ThreadSender(String nick, byte[] nickBytes, DatagramSocket dgramSocket) {
        try {
            this.dgramSocket = dgramSocket; //cria um socket datagrama
            this.nick = nick;
            this.nickBytes = nickBytes;

        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    //execução principal
    @Override
    public void run(){

        try {
            Scanner reader = new Scanner(System.in);

            //recebe o IP
            System.out.println("IP Destino: ");
            String dstIP = reader.nextLine();
            int dstPort = 6666;
            
            // armazena o IP do destino
            InetAddress serverAddr = InetAddress.getByName(dstIP);
            // porta do servidor
            int serverPort = dstPort; 

            do {
                //transforma o nick do usuário em bytes
                byte[] nick = new byte[this.nickBytes.length];
                nick = this.nick.getBytes();

                //armazena a mensagem
                System.out.println("Mensagem: ");
                String msg = reader.nextLine();

                //transforma a mensagem em bytes
                byte[] m = msg.getBytes();
                byte[] mSize = new byte[] {(byte)m.length};

                /*gera o pacote adicionando o
                    tamanho do nome
                    o nome
                    tamanho da mensagem
                    mensagem
                */
                byte[] packageToSend = new byte [this.nickBytes.length + nick.length + mSize.length + m.length];
                System.arraycopy(this.nickBytes, 0, packageToSend, 0, this.nickBytes.length);
                System.arraycopy(nick, 0, packageToSend, this.nickBytes.length, nick.length);
                System.arraycopy(mSize, 0, packageToSend, (this.nickBytes.length + nick.length), mSize.length);
                System.arraycopy(m, 0, packageToSend, (this.nickBytes.length + nick.length + mSize.length), m.length);

                /* cria um pacote datagrama */
                DatagramPacket request
                        = new DatagramPacket(packageToSend, packageToSend.length, serverAddr, serverPort);

                /* envia o pacote */
                this.dgramSocket.send(request);

                System.out.println("Nova mensagem? (Y/N): ");
                this.resp = reader.nextLine();

            } while (this.resp.equals("N") || this.resp.equals("n") != true);

            /* libera o socket */
            this.dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        } //catch
    }
}