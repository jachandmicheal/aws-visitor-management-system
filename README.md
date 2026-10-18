# Visitor Management System on AWS

## 1. Project Overview

This project is a web-based Visitor Management System for an office. It is built with Python Flask and deployed on an Amazon Web Services (AWS) EC2 Linux server. Visitor records are stored in an Amazon DynamoDB table. Reception staff can check visitors in and out, and view the visitor log by month, date, and hour.

## 2. Objectives

- To launch an AWS EC2 Linux instance and make it reachable over HTTP.
- To create a DynamoDB table that stores visitor records.
- To give the server access to DynamoDB securely using an IAM role (no passwords in the code).
- To build a Flask web application for visitor check-in and check-out.
- To filter and sort the visitor log by month, date, hour, and time.
- To keep the application running automatically using a systemd service.

## 3. Technologies Used

- **Cloud Platform:** AWS (EC2, DynamoDB, IAM)
- **Operating System:** Amazon Linux 2023
- **Programming Language:** Python 3
- **Web Framework:** Flask
- **AWS SDK:** boto3
- **Database:** Amazon DynamoDB
- **Process Manager:** systemd
- **Frontend:** HTML and CSS (Jinja2 templates)
- **AWS Region:** ap-southeast-2 (Sydney)

## 4. System Architecture

**User Browser → AWS EC2 (Flask app on port 80) → Amazon DynamoDB**

The EC2 instance uses an IAM role (`VisitorAppRole`) with DynamoDB access, so the application reads and writes the `Visitors` table without storing any credentials. A security group allows SSH (port 22) for administration and HTTP (port 80) for the website.

## 5. Features

- Visitor check-in with name, person to meet, and purpose of visit.
- One-click check-out that records the exit time.
- Filter the log by **month**, **date**, and **hour** (12 AM to 11 PM).
- Sort by **newest first** or **oldest first**, using the full date and time.
- Records grouped by month and year, then by day, with times shown as hours and minutes.
- Live count of the visitors shown.
- Times displayed in Indian Standard Time (IST).

## 6. Database Design

| Item | Value |
| --- | --- |
| Table name | `Visitors` |
| Partition key | `visitor_id` (String) |
| Attributes | `name`, `host`, `purpose`, `check_in`, `check_out` |

`check_in` and `check_out` are stored as `YYYY-MM-DD HH:MM:SS` text, which keeps date and time sorting simple and accurate.

## 7. Project Structure

- `app.py` — Main Flask application (routes, DynamoDB access, page template).
- `requirements.txt` — Python dependencies.
- `screenshots/` — Project screenshots.
- `README.md` — Project documentation.
- `.gitignore` — Files excluded from Git.

## 8. Deployment Steps

1. Sign in to the AWS Console and use the Sydney (ap-southeast-2) region.
2. Create a DynamoDB table named `Visitors` with partition key `visitor_id` (String).
3. Create an IAM role for EC2 (`VisitorAppRole`) with the DynamoDB full access policy.
4. Launch an EC2 instance (Amazon Linux 2023, free-tier eligible type) and attach `VisitorAppRole` under Advanced details.
5. Configure the security group to allow SSH (port 22) and HTTP (port 80) from anywhere.
6. Connect to the instance using EC2 Instance Connect.
7. Install the dependencies:
   ```bash
   sudo dnf install -y python3-pip
   sudo pip3 install -r requirements.txt
   ```
8. Add `app.py` to the server and test it:
   ```bash
   sudo python3 app.py
   ```
9. Create a systemd service (`/etc/systemd/system/visitor.service`) so the app starts on boot and restarts on failure:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now visitor
   ```
10. Open `http://<EC2-PUBLIC-IPV4-ADDRESS>` in a browser.

## 9. Screenshots

Add your screenshots to the `screenshots/` folder and update the file names below.

| Screenshot | Description |
| --- | --- |
| `screenshots/website.png` | Visitor Management System web page |
| `screenshots/filters.png` | Month, date, hour filters and sorting |
| `screenshots/ec2-instance.png` | Running EC2 instance with public IP |
| `screenshots/dynamodb-table.png` | Visitor records in DynamoDB |
| `screenshots/security-group.png` | Inbound rules (SSH and HTTP) |

## 10. Result

The Visitor Management System was successfully deployed on an AWS EC2 Linux server. Visitors can be checked in and out through the website, and every record is saved in Amazon DynamoDB. The log can be filtered by month, date, and hour and sorted by time. The systemd service keeps the website running continuously.

## 11. Limitations and Future Improvements

- The site uses HTTP only. HTTPS can be added with a domain name and a certificate.
- The app runs on Flask's built-in server, which is fine for a demo. For production use, run it with Gunicorn behind Nginx.
- Add a login for reception staff.
- Add visitor photo and ID capture.
- Send an email or notification to the host when a visitor arrives.

## 12. Conclusion

This project provides practical experience with cloud computing on AWS, including EC2 server setup, DynamoDB database design, IAM roles for secure access, Linux service management, and Python web development with Flask.

## 13. References

1. AWS EC2 Documentation: <https://docs.aws.amazon.com/ec2/>
2. Amazon DynamoDB Documentation: <https://docs.aws.amazon.com/dynamodb/>
3. AWS IAM Documentation: <https://docs.aws.amazon.com/iam/>
4. Flask Documentation: <https://flask.palletsprojects.com/>
5. Boto3 Documentation: <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>
6. GitHub Documentation: <https://docs.github.com/>
