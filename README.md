# spark-k8s-v322
Spark for spark operator on k8s in version 3.2.2.

1. Build Spark Image from binaries
- Acess below link and download the binaries in version 'spark-3.2.2-bin-hadoop3.2'.
https://spark.apache.org/downloads.html

- Unzip the binaries, open the file:
"\spark-3.2.2-bin-hadoop3.2\kubernetes\dockerfiles\spark\Dockerfile"

- Add permissions to /opt/spark adding the following command after line 58:
"RUN chmod g+rwx -R /opt/spark"
This permission avoid erros to use sc.addPyFile() commands to read zips from s3.

- Navigate to binaries root folder, and build images following the doc below:
https://spark.apache.org/docs/3.2.2/running-on-kubernetes.html#docker-images

2. Push base image to your repo
- In this case, I push a clean image created after last step. Pay attention in the tag used to build.

3. Customize jars from Delta, AWS Hadoop etc.
- In this repo I place common jars for interact with AWS and Delta Lake. Build image using the dockerfile located in root folder of this repo.
Adjust the base image of your dockerfile to the tag builded and pushed in the last steps.

List of jars used in this repo:
- aws-java-sdk-bundle-1.11.901.jar (download this jar from maven, the size doesn't allow upload this to github)
- delta-core_2.12-2.0.0.jar
- delta-storage-2.0.0.jar
- hadoop-aws-3.3.1.jar
- hadoop-common-3.3.1.jar
- hadoop-mapreduce-client-core-3.3.1.jar
- spark-hadoop-cloud_2.12-3.3.0.jar

Insert others jars in the folder before build a new image. In my dockerfile I use some parameters to deliver AWS access and secret keys, in case of you don't use, remove them.
If you use different python libs, insert them on requirements.txt file.

4. Use the ConfigSpark.yaml to submit your application on k8s and test your image. Peace!