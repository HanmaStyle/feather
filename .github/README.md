# Signa

Signa — нативный менеджер подписи и установки iOS-приложений с тёплым оранжевым акцентом и системным Liquid Glass. Проект является производной версией [Feather](https://github.com/claration/Feather) и сохраняет лицензию GPL-3.0.

## Возможности

- Импорт IPA/TIPA из «Файлов» и по URL.
- Подпись приложений на устройстве через Zsign с собственными P12 и mobileprovision.
- Установка подписанных приложений через IDevice/installd и локальный сервер.
- Настройка Bundle ID, названия, версии, иконки и entitlements.
- Внедрение `.deb` и `.dylib` через Ellekit.
- AltStore-источники, поиск и проверка обновлений.
- Библиотека импортированных и подписанных приложений, управление сертификатами и файлами.
- Liquid Glass на iOS 26/27 и Material fallback на более ранних поддерживаемых системах.

## Сборка через GitHub Actions

Workflow использует runner `xcode-27` и запускается после push в `main`, по тегу `v*` или вручную через **Actions → Build Signa IPA → Run workflow**.

Без Secrets создаётся `Signa-unsigned.ipa`. Этот файл предназначен только для последующей подписи и не является готовым установочным IPA.

### Получение подписанного Signa.ipa

Добавьте в **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Содержимое |
| --- | --- |
| `SIGNING_P12_BASE64` | Ваш P12 в Base64, одной строкой |
| `SIGNING_P12_PASSWORD` | Пароль от P12 |
| `SIGNING_MOBILEPROVISION_BASE64` | Ваш mobileprovision в Base64, одной строкой |

Сертификат и provisioning profile должны принадлежать вам, быть действительными и разрешать Bundle ID `com.hanmastyle.signa` либо соответствующий wildcard App ID. UDID устройства должен быть зарегистрирован для development/ad-hoc profile.

На Mac Base64 можно получить командами:

```sh
base64 -i certificate.p12 | pbcopy
base64 -i profile.mobileprovision | pbcopy
```

После успешного запуска скачайте artifact **Signa-v…-signed**, внутри которого находится `Signa.ipa`. Временный keychain и расшифрованные сертификаты удаляются после шага подписи. Не добавляйте исходные сертификаты в репозиторий и не публикуйте их в Issues.

## Локальная сборка на Mac

```sh
git submodule update --init --recursive
make iphoneos
```

## Исходный проект и благодарности

- [Feather / Samara](https://github.com/claration/Feather) — исходный интерфейс и архитектура приложения.
- [Zsign](https://github.com/zhlynn/zsign) — подпись на устройстве.
- [idevice](https://github.com/jkcoxson/idevice) — взаимодействие с `installd`.
- [Ellekit](https://github.com/tealbathingsuit/ellekit) — внедрение tweaks.
- [Nuke](https://github.com/kean/Nuke) — загрузка и кеширование изображений.

Полный текст лицензии находится в [LICENSE](../LICENSE). Изменённый исходный код Signa распространяется на условиях GPL-3.0.
