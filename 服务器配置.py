import socket
import logging

def check_server_accessibility(ip, port=22, timeout=5):
    """
    检查服务器的网络连通性
    :param ip: 服务器IP地址
    :param port: 服务器端口，默认为SSH端口22
    :param timeout: 连接超时时间，默认为5秒
    :return: 布尔值，表示服务器是否可访问
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            logging.info(f"服务器{ip}端口{port}可访问")
            return True
        else:
            logging.warning(f"服务器{ip}端口{port}不可访问，错误码：{result}")
            return False
    except socket.error as e:
        logging.error(f"检查服务器{ip}时发生错误：{e}")
        return False
    finally:
        sock.close()


        version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: always
    ports:
      - "9000:9000"
      - "8000:8000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    networks:
      - portainer_network

  portainer_agent:
    image: portainer/agent:latest
    container_name: portainer_agent
    restart: always
    environment:
      AGENT_CLUSTER_ADDR: tasks.portainer_agent
    ports:
      - "9001:9001"
    volumes:
      /var/run/docker.sock:/var/run/docker.sock
      /var/lib/docker/volumes:/var/lib/docker/volumes
    command: --tlsskipverify
    deploy:
      mode: global
    networks:
      - portainer_network

networks:
  portainer_network:
    driver: overlay

volumes:
  portainer_data: