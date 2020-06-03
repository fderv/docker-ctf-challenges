# brute-force-registration

Flask web app containerized in Docker.
Created as a CTF challenge.

Solution:
Hacker needs to register the website. In order to do this, he/she must know the registration code. This could be bypassed by brute-force or dictionary attack. However, the website prompts a captcha after 5th registration attempt. Attempt count is stored in client side as a cookie. This value must be manipulated by the attacher.
When registration is completed, the flag can be found by logging in.

To run:
docker-compose up --build