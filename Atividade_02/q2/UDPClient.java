import java.io.*;
import java.math.BigInteger;
import java.util.*;
import java.net.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.ByteBuffer;
import java.nio.file.Files;

public class UDPClient {

    DatagramSocket dgramSocket;
    DatagramPacket dgramPackage;
    int serverPort = 6666;
    InetAddress serverAddr;

    public UDPClient(){
        try {
            Scanner reader = new Scanner(System.in);

            //Cria socket de UDP
            this.dgramSocket = new DatagramSocket(this.serverPort);;
            
            /* armazena o IP do destino */
            System.out.println("IP Destino: ");
            String dstIP = "192.168.56.102";
            this.serverAddr = InetAddress.getByName(dstIP);

            run();

        } catch (Exception e) {
            // TODO: handle exception
        }
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

    public void sendPackage (byte[] payload, int payloadSize){
        this.dgramPackage = new DatagramPacket(payload, payloadSize, this.serverAddr, this.serverPort);

        /* envia o pacote */
        try {
            this.dgramSocket.send(this.dgramPackage);
        } catch (Exception e) {
            //TODO: handle exception
        }
    }

    public void splitFile(File f) throws IOException {
        
        int partCounter = 1;
        int sizeOfFiles = 1024;
        
        byte[] buffer = new byte[sizeOfFiles];

        String fileName = f.getName();

        if (fileName != null) {
            try (
                FileInputStream fis = new FileInputStream(f); 
            BufferedInputStream bis = new BufferedInputStream(fis)
            ) {
                byte[] md5 = new byte[1024];
                try {
                    //calcula o md5 do arquivo
                    md5 = checksum(fileName);   
                } catch (Exception e) {
                    //TODO: handle exception
                }
                
                System.out.println("Md5: " + md5);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o md5 do arquivo total para o servidor
                sendPackage(md5, md5.length);
                
                //calcula a quantidade de pacotes a serem enviados
                long qtdOfPckg = (f.length()/buffer.length) + 1;
 
                System.out.println("Quantidade de pacotes: " + qtdOfPckg);
                
                //insere o Long no byte[]
                String qtdBuffer = String.valueOf(qtdOfPckg);
                try {
                    Thread.sleep(100);
                    
                } catch (Exception e) {
                    //TODO: handle exception
                }
                //envia o número de pacotes que o servidor deve ler
                sendPackage(qtdBuffer.getBytes(), qtdBuffer.getBytes().length);
                
                
                int bytesAmount = 0;
                while ((bytesAmount = bis.read(buffer)) > 0) {
                    try {
                        Thread.sleep(100);
                        
                    } catch (Exception e) {
                        //TODO: handle exception
                    }
                    sendPackage(buffer, bytesAmount);
                    System.out.println("payload: " + buffer);
    
                }
                System.out.println("Arquivo enviado com sucesso.");
            }
        } else {
            System.out.println("Não foi possível encontrar um arquivo com esse nome, digite um nome existente.");
        }
    }

    public void run() {

        Scanner reader = new Scanner(System.in);

        try {

            String resp = "";

            do {

                
                System.out.println("Digite o nome do arquivo e a extensão: ");
                String fileName = reader.nextLine();

                File f = new File(fileName);

                byte[] fileNameBytes = fileName.getBytes(); // transforma o nome do arquivo em bytes
                byte[] fileSize = new byte[32];

                // System.arraycopy(fileSize, 0, f.length(), 0, arg4);

                sendPackage(fileNameBytes, fileNameBytes.length);
                // sendPackage(, payloadSize);

                splitFile(f);

                System.out.println("Novo arquivo? (Y/N): ");
                resp = reader.nextLine();

            } while (resp.equals("N") || resp.equals("n") != true);

            /* libera o socket */
            dgramSocket.close();
        } catch (SocketException e) {
            System.out.println("Socket: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("IO: " + e.getMessage());
        }

    }
    
    public static void main(String[] args) {
        UDPClient client = new UDPClient();
    }
}
