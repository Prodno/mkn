# PROTO SCHEMA

В этой задаче вам дан сгенерированный `protoc==3.11.1` код. Необходимо по данному коду понять, какая была изначальная схема, и записать ее в файлик `schema.proto`.

### Установка `protoc`

```bash
PROTOC_ZIP=protoc-3.11.1-linux-x86_64.zip  # или protoc-3.11.1-osx-x86_64.zip для Mac
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.11.1/$PROTOC_ZIP
sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*'
sudo chmod +x /usr/local/bin/protoc
rm -f $PROTOC_ZIP
```
