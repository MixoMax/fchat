import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.impl.client.HttpClientBuilder;

public class fchat {
    //define ip and port
    public static final String ip = "localhost";
    public static final int port = 5000;

    public static void main(String[] args) {
        sendMessage("my_chat_id", "my_sender", "my_message", "my_password");
    }
    
    public static void sendMessage(String chat_id, String sender, String message, String password) {
        HttpClient client = HttpClientBuilder.create().build();
        HttpPost post = new HttpPost(getEndpointUrl("/send"));
        post.setEntity(buildFormData(chat_id, sender, message, password));
        
        try {
            HttpResponse response = client.execute(post);
            System.out.println("Message sent: " + response);
        } catch (IOException e) {
            System.err.println("Error sending message: " + e.getMessage());
        }
    }
    
    private static URI getEndpointUrl(String path) {
        try {
            return new URI("http", null, ip, port, path, null, null);
        } catch (URISyntaxException e) {
            throw new RuntimeException(e);
        }
    }
    
    private static MultipartEntityBuilder buildFormData(String chat_id, String sender, String message, String password) {
        MultipartEntityBuilder builder = MultipartEntityBuilder.create();
        builder.addTextBody("chat_id", chat_id);
        builder.addTextBody("sender", sender);
        builder.addTextBody("message", message);
        builder.addTextBody("password", password);
        builder.addTextBody("timestamp", String.valueOf(System.currentTimeMillis() / 1000));
        builder.setContentType(ContentType.MULTIPART_FORM_DATA);
        return builder;
    }
}
