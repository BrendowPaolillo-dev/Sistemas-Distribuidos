import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.util.Arrays;

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
        byte[] buffer = new byte[1024]; // cria um buffer para receber requisições
        this.dgramPacket = new DatagramPacket(buffer, buffer.length);
        
        run();
    }

    public byte[] checksum(String fileName) throws Exception{
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
        return complete.digest();
    }

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
                        byte[] md5Real = this.dgramPacket.getData();
                        byte[] md5Calc = new byte[1024];
                        System.out.println("Recebi o Md5");
                        
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

                            System.out.println("sizePackage: " + sizePackage);
                            System.out.println("Payload: " + payload );

                            //escreve o arquivo na pasta
                            try (FileOutputStream fos = new FileOutputStream("./"+fileName, true)) {
                                fos.write(payload, 0, sizePackage);
                                fos.close();
                            }
                            i++;
                            
                        } // while
                        //calcula o md5 do arquivo recebido
                        md5Calc = checksum(fileName);
                        System.out.println("Resultado da comparacao do Md5: " + Arrays.equals(md5Real, md5Calc));

                        if (Arrays.equals(md5Calc, md5Real) == true){
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
        UDPServer server = new UDPServer();
    }
}
