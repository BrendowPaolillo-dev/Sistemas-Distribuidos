import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.util.Arrays;

/*
    Sistema de transferência de arquivos via UDP
    Desenvolvedores: Brendow e Lucas

    Classe:     Servidor

    Execução:   javac UDPServer.java
                java UDPServer

    Funcionamento:  O programa aguarda a conexão do cliente;
                    Recebe o nome do arquivo;
                    Armazena os bytes recebidos;
                    Concatena os bytes recebidos em um arquivo;
                    Calcula o Md5 do arquivo completo;
                    Compara o Md5 recebido com o calculado;
                    E finaliza a execução ao final da transferência.
*/

public class UDPServer {
    DatagramSocket dgramSocket;
    DatagramPacket dgramPacket;

    public UDPServer() {
        try {
            // cria um socket datagrama em uma porta especifica
            this.dgramSocket = new DatagramSocket(6666);
        } catch (Exception e) {
            //TODO: handle exception
        }
        // cria um buffer para receber requisições
        byte[] buffer = new byte[1024]; 
        this.dgramPacket = new DatagramPacket(buffer, buffer.length);
        
        run();
    }

    //converte um vetor de bytes para uma string de Hexadecimais
    public StringBuilder convertToHexa(byte[] bytes){

        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < bytes.length; i++) {

            sb.append(Integer
                    .toString((bytes[i] & 0xff) + 0x100, 16)
                    .substring(1));
        }

        return sb;
    }

    //realiza a criação do código de verificação (md5), 
    //para garantir a integridade do arquivo
    public String checksum(String fileName) throws Exception{
        InputStream fis =  new FileInputStream(fileName);

        byte[] buffer = new byte[1024];
        MessageDigest complete = MessageDigest.getInstance("MD5");
        int numRead;

        do {
            numRead = fis.read(buffer);
            if (numRead > 0) {
                complete.update(buffer, 0, numRead);
            }
        } while (numRead != -1);

        fis.close();

        StringBuilder sb = convertToHexa(complete.digest());
        
        return sb.toString();
    }

    //execução principal
    public void run(){
        try {
            
            try {
                //Recebe o nome do arquivo a ser transferido
                this.dgramSocket.receive(this.dgramPacket);
                byte[] fileNameBytes = this.dgramPacket.getData();
                String fileName = new String(fileNameBytes, 0, this.dgramPacket.getLength());
                System.out.println("Nome do arquivo: " + fileName);
                
                //Se tiver um nome de arquivo
                if (fileName != null){

                    try {

                        //Recebe o md5 do arquivo
                        this.dgramSocket.receive(this.dgramPacket);
                        byte[] md5RealBytes = this.dgramPacket.getData();
                        String md5Real = new String(md5RealBytes, 0, this.dgramPacket.getLength());
                        String md5Calc = "";

                        //Recebe a quantidade de pacotes a serem recebidos
                        this.dgramSocket.receive(this.dgramPacket);
                        byte[] qtdBuffer = this.dgramPacket.getData();
                        String strQtd = new String(qtdBuffer, 0, this.dgramPacket.getLength());
                        long qtdOfPckg = Long.valueOf(strQtd);
                        System.out.println("Quantidade de pacotes a serem recebidos: " + qtdOfPckg);
                        
                        long i = 0;

                        while (i < qtdOfPckg) {

                            //recebe a carga de dados do UDP
                            this.dgramSocket.receive(this.dgramPacket);
                            byte[] payload = this.dgramPacket.getData();
                            int sizePackage = this.dgramPacket.getLength();
                            
                            System.out.println("Payload: " + payload );

                            //escreve o arquivo na pasta e faz o append dos bytes
                            try (FileOutputStream fos = new FileOutputStream("./"+fileName, true)) {
                                fos.write(payload, 0, sizePackage);
                                fos.close();
                            }
                            i++;
                            
                        }

                        //calcula o md5 do arquivo recebido
                        md5Calc = checksum(fileName).toString();
                        System.out.println("MD5 Calc: " + md5Calc + "\nMD5 Real: " + md5Real);
                        System.out.println("Resultado da comparacao do Md5: " + md5Calc.equals(md5Real));

                        //verifica se o valor calculado é igual ao recebido
                        if (md5Calc.equals(md5Real)){
                            System.out.println("Arquivo recebido com sucesso.");
                        }else{
                            System.out.println("A verificação de soma falhou.");
                        }

                    } catch (Exception e) {
                        //TODO: handle exception
                    }
                }
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
        System.out.println("Finalizada a transferência.");
    }

    public static void main(String[] args) {
        System.out.println("Server iniciado.");
        UDPServer server = new UDPServer();
    }
}
