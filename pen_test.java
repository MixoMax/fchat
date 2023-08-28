//make 1000 http void requests to localhost:80/api/ping
//and print the total time taken
//to compile: javac -cp .:lib/* pen_test.java
//to run: java -cp .:lib/* pen_test
import java.io.*;
import java.net.*;

//for multithreading
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.Callable;

public class pen_test {
    public static void main(String[] args) throws Exception {
        int num_requests = 1000;
        //make_request("create_chat/2/*", 1);
        //create_thread("ping", num_requests);
        //create_thread("static/css/style.css", num_requests);
        //create_thread("static/js/chat.js", num_requests);
        create_thread("send_message", num_requests);
        //create_thread("get_chat/2", 25);
        //create_thread("get_chat_uncached/2", 25);
    }
    //void function to make a http request to an endpoint
    public static void make_request(String endpoint, int num_requests) throws Exception {
        String api_url = "http://localhost:80/api/" + endpoint;
        URL url = new URL(api_url);
        for (int i = 0; i < num_requests; i++) {
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");
            int status = con.getResponseCode();
            if (status != 200 && status != 308) {
                System.out.println("Error: " + status + " in " + endpoint);
            }
            con.disconnect();
        }

    }

    public static void make_post_request(String endpoint, int num_requests) throws Exception {
        String api_url = "http://localhost:80/api/" + endpoint;
        URL url = new URL(api_url);

        //headers = {"content-type": "application/json"}
        //charset = "utf-8"
        //data = {"chat_id": "2", "sender": "pen_test", "content": "this is a test", "response_to": ""}

        for (int i = 0; i < num_requests; i++) {
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("content-type", "application/json");
            con.setDoOutput(true);
            String jsonInputString = "{\"chat_id\": \"2\", \"sender\": \"pen_test\", \"content\": \"this is a test\", \"response_to\": \"\"}";
            try (OutputStream os = con.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }
            int status = con.getResponseCode();
            if (status != 200 && status != 308) {
                System.out.println("Error: " + status + " in " + endpoint);
            }
            con.disconnect();
        }
    }

    public static void create_thread(String endpoint, int num_requests) throws Exception {
        long start = System.currentTimeMillis();
        ExecutorService executor = Executors.newFixedThreadPool(num_requests);
        Callable<String> callable = new Callable<String>() {
            @Override
            public String call() throws Exception {
                if (endpoint == "send_message") {
                    make_post_request(endpoint, 1);
                    return "Done";
                } else {
                    make_request(endpoint, 1);
                    return "Done";
                }
            }
        };
        for (int i = 0; i < num_requests; i++) {
            executor.submit(callable);
        }
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.DAYS);

        long end = System.currentTimeMillis();
        long time_per_request = (end - start) / num_requests;
        System.out.println(endpoint + " took " + time_per_request + "ms per request");
    }
}
