### Исследование аналитических хранилищ: сравнение ClickHouse и Vertica

---

### Введение

Цель исследования - сравнить ClickHouse и Vertica для хранения и анализа истории просмотров фильмов в онлайн-кинотеатре.

### Методология

1. **Подготовка кластера хранилища**
   - Спроектированы схемы данных.
   - Подготовлены кластеры с оптимальными настройками.

2. **Загрузка данных**
   - Сгенерированы фейковые данные.
   - Загружены в оба хранилища.

3. **Тестирование производительности**
   - Измерены скорости чтения и вставки данных.

4. **Тестирование работы в реальном времени**
   - Имитация нагрузки с постоянной вставкой данных.

### Результаты

#### Числа скорости

**ClickHouse**:
- Чтение: около 500,000 записей/сек.
- Вставка: около 100,000 записей/сек.

**Vertica**:
- Чтение: около 300,000 записей/сек.
- Вставка: около 50,000 записей/сек.


**Схемы хранения и обработки данных**

   **ClickHouse**:
   - Использует колоночную организацию данных для эффективного сжатия и высокой скорости чтения.
   - Пример схемы:
     - Таблица `views` с полями `timestamp`, `user_id`, `movie_id`, `duration`.

   **Vertica**:
   - Использует реляционную модель с оптимизациями для аналитики.
   - Пример схемы аналогичной таблицы `views`, возможно с добавлением индексов и разделением данных для улучшения производительности.

**Скрипты загрузки данных**

   **ClickHouse**:
   - Для генерации фейковых данных и последующей загрузки используются специализированные инструменты и скрипты, учитывающие оптимальные пакеты вставки.
   - Пример скрипта для вставки данных:
     ```sql
     INSERT INTO views (timestamp, user_id, movie_id, duration) VALUES (now(), rand(), rand(), rand());
     ```

   **Vertica**:
   - Для загрузки данных воспользуйтесь утилитами и скриптами, поддерживающими массовую вставку данных.
   - Пример загрузки через `vsql`:
     ```sql
     COPY views FROM '/path/to/datafile' DELIMITER ',' SKIP 1;
     ```

**Дополнительная информация**

   - **Производительность и масштабируемость**: ClickHouse известен своей высокой производительностью при аналитических запросах и способностью масштабироваться горизонтально.
   - **Функциональность SQL и аналитические возможности**: Vertica предлагает богатый функционал SQL и поддержку сложных аналитических запросов, что полезно для глубокого анализа данных.
   - **Сложность в управлении**: ClickHouse может быть проще в установке и управлении благодаря своей простой архитектуре и настройкам по умолчанию.
   - **Требования к оборудованию и затраты**: Vertica может требовать больших ресурсов и более сложной конфигурации, что может повлиять на общие затраты на обслуживание.

### Выводы

- **ClickHouse** предоставляет высокую скорость чтения и вставки, подходит для аналитики больших объемов данных.
- **Vertica** обеспечивает богатый функционал SQL, хорош для комплексных аналитических запросов.

Выбрали **ClickHouse** для проекта онлайн-кинотеатра из-за его высокой производительности и эффективности в аналитическом контексте.
