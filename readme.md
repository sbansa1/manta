# Manta Assignment

#### Project Details

```text
Clone the project using the command:

git clone .. 

once the project is cloned

Run Docker 

Docker-compose up -d --build

once all the dependencies are installed and running properly

Execute the command to re-create db:

docker-compose exec event-service python manage.py  "recreate_db"
docker-compose exec event-service python manage.py  "seed_db"

To format the code : 
docker-compose exec event-service blake8 app --check

docker-compose exec event-service blake8 app --diff

For linting and inspect code quality:

docker-compose exec event-service flake8 app


The seed_db and recreate_db will seed the database.

In case if you want to make any changes in the Env Variables

you can directly change them by browsing the docker-compose file.



I know I am late :) but I tried and to handle the operator I could have made a decorator and defined rules for admin.

I am not sure if project meet your requirements.

In production I would have used rabbitmq to establish an event-store probably for better monitoring and control.

I have not created any test cases.







