#include <iostream>
#include <string>
#include <curl/curl.h>
#include <boost/thread.hpp>
#include <chrono>



void make_request(std::string url, int num_requests) {
    CURL *curl;
    CURLcode res;
    curl = curl_easy_init();
    if (curl) {
        for (int i = 0; i < num_requests; i++) {
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
            res = curl_easy_perform(curl);
        }
        curl_easy_cleanup(curl);
    }
}

int main() {
    double start_time = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()).count();
    std::string api_url = "http://localhost:80/api/ping";
    int num_requests = 1000;
    int num_threads = 10;
    int requests_per_thread = (int) num_requests / num_threads;

    // Setup 10 threads to make api calls in parallel
    boost::thread_group threads;
    for (int i = 0; i < num_threads; i++) {
        threads.create_thread(boost::bind(&make_request, api_url, requests_per_thread));
    }
    threads.join_all();

    double time_delta = std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()).count() - start_time;

    std::cout << num_requests << " requests made in" << (int) time_delta << " ms" << std::endl;

    return 0;
}