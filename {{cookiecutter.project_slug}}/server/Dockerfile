FROM nginx:1-alpine

EXPOSE 80
EXPOSE 443

COPY entrypoint.sh /
COPY nginx.conf /etc/nginx/conf.d/default.template
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]