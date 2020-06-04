FORM 基础镜像，当前新镜像是基于哪个镜像的
MAINTAINER 镜像维护者的姓名和邮箱
RUN 容器构建时需要运行的命令
EXPOSE 当前容器对外暴露出的端口
WORKDIR 指定在创建容器后，终端默认登陆进来的工作目录，一个落脚点
ENV 用来在构建镜像过程中设置环境变量
ADD 将宿主机目录下的文件拷贝进镜像且ADD命令会自动处理URL和解压tar压缩包
COPY 类似ADD，拷贝文件和目录到镜像中，注意这个不会解压
VOLUME 容器数据卷，用于数据保存和持久化操作
CMD 指定一个容器启动时要运行的命令，dockerfile可以有多个cmd，但是只有最后一个生效
ENTRYPOINT 指定一个容器启动时要运行的命令，不会被覆盖，会追加
ONBUILD 当构建一个被继承的Dockerfile时运行命令，父镜像在被子继承后父镜像的onbuild会被触发，类似于一个触发器

FROM centos

RUN yum -y install crul

ENTRYPOINT["curl", "-s", "http://ip.cn"]