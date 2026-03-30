<template>
  <div>
    <!-- Заголовок и панель управления -->
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        color: black;
      ">
      <div style="display: flex; gap: 10px">
        <!-- Расширенная строка поиска -->
        <div style="display: flex; gap: 5px">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по серийному номеру, типу или результату..."
            style="
              padding: 8px 12px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
              width: 350px;
              background-color: white;
              color: black;
            " />
        </div>

        <!-- Кнопка фильтра -->
        <button
          @click="showFilters = !showFilters"
          style="
            background-color: white;
            border: 1px solid #e0e0e0;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
            color: black;
          ">
          <span>⚙️</span> Фильтр
        </button>

        <!-- Кнопка добавления (доступна всем) -->
        <button
          @click="openAddModal"
          style="
            background-color: black;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
          ">
          <span style="font-size: 18px">+</span> Добавить
        </button>

        <!-- Кнопка обновления -->
        <button
          @click="loadVerifications"
          :disabled="loading"
          style="
            background-color: white;
            color: black;
            border: 1px solid #e0e0e0;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 5px;
          ">
          <span>🔄</span> {{ loading ? "Загрузка..." : "Обновить" }}
        </button>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" style="text-align: center; padding: 40px; color: #666">
      Загрузка данных...
    </div>

    <!-- Панель фильтров -->
    <div
      v-if="showFilters"
      style="
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
      ">
      <div
        style="
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          margin-bottom: 15px;
        ">
        <!-- Фильтр по статусу -->
        <div>
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 12px;
              color: #666;
            "
          >Статус</label
          >
          <select
            v-model="filters.completed"
            style="
              width: 100%;
              padding: 8px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            ">
            <option value="all">Все статусы</option>
            <option value="completed">Завершенные</option>
            <option value="pending">Незавершенные</option>
          </select>
        </div>

        <!-- Фильтр по результату -->
        <div>
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 12px;
              color: #666;
            "
          >Результат</label
          >
          <select
            v-model="filters.resultId"
            style="
              width: 100%;
              padding: 8px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            ">
            <option value="all">Все результаты</option>
            <option
              v-for="result in results"
              :key="result.id"
              :value="result.id">
              {{ result.result_name }}
            </option>
          </select>
        </div>

        <!-- Фильтр по типу поверки -->
        <div>
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 12px;
              color: #666;
            "
          >Тип поверки</label
          >
          <select
            v-model="filters.typeId"
            style="
              width: 100%;
              padding: 8px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            ">
            <option value="all">Все типы</option>
            <option
              v-for="type in verificationTypes"
              :key="type.id"
              :value="type.id">
              {{ type.type_name }}
            </option>
          </select>
        </div>

        <!-- Фильтр по планируемой дате с -->
        <div>
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 12px;
              color: #666;
            "
          >План. дата с</label
          >
          <input
            type="date"
            v-model="filters.plannedFrom"
            style="
              width: 100%;
              padding: 8px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            " />
        </div>

        <!-- Фильтр по планируемой дате по -->
        <div>
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 12px;
              color: #666;
            "
          >План. дата по</label
          >
          <input
            type="date"
            v-model="filters.plannedTo"
            style="
              width: 100%;
              padding: 8px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            " />
        </div>
      </div>

      <div style="display: flex; gap: 10px; justify-content: flex-end">
        <button
          @click="resetFilters"
          style="
            padding: 6px 12px;
            background-color: white;
            color: black;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
          ">
          Сбросить фильтры
        </button>
        <button
          @click="applyFilters"
          style="
            padding: 6px 12px;
            background-color: black;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
          ">
          Применить
        </button>
      </div>
    </div>

    <!-- Таблица -->
    <div
      v-if="!loading"
      style="overflow-x: auto; border: 1px solid #e0e0e0; border-radius: 8px">
      <table style="width: 100%; border-collapse: collapse; font-size: 14px">
        <thead>
          <tr
            style="background-color: #f5f5f5; border-bottom: 2px solid #e0e0e0">
            <th style="padding: 12px 15px; text-align: left">ID</th>
            <th style="padding: 12px 15px; text-align: left">Серийный номер</th>
            <th style="padding: 12px 15px; text-align: left">Тип поверки</th>
            <th style="padding: 12px 15px; text-align: left">Статус</th>
            <th style="padding: 12px 15px; text-align: left">Результат</th>
            <th style="padding: 12px 15px; text-align: left">Плановая дата</th>
            <th style="padding: 12px 15px; text-align: left">
              Фактическая дата
            </th>
            <th style="padding: 12px 15px; text-align: left">Метролог</th>
            <th style="padding: 12px 15px; text-align: center">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in filteredData"
            :key="item.id"
            style="border-bottom: 1px solid #e0e0e0">
            <td style="padding: 12px 15px">{{ item.id }}</td>
            <td style="padding: 12px 15px">{{ item.instrument_serial }}</td>
            <td style="padding: 12px 15px">{{ item.type_name || "—" }}</td>
            <td style="padding: 12px 15px">
              <select
                v-if="canEditStatus(item)"
                v-model="item.is_completed"
                @change="updateStatus(item)"
                style="
                  padding: 4px 8px;
                  border: 1px solid #e0e0e0;
                  border-radius: 4px;
                  font-size: 12px;
                ">
                <option :value="false">В процессе</option>
                <option :value="true">Завершена</option>
              </select>
              <span
                v-else
                :style="{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontWeight: '500',
                  backgroundColor: item.is_completed ? '#e8f5e8' : '#fff4e5',
                  color: item.is_completed ? '#2e7d32' : '#f57c00',
                }">
                {{ item.is_completed ? "Завершена" : "В процессе" }}
              </span>
            </td>
            <td style="padding: 12px 15px">
              <span
                v-if="item.result_name"
                :style="{
                  padding: '4px 8px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontWeight: '500',
                  backgroundColor:
                    item.result_name === 'Поверка пройдена'
                      ? '#e8f5e8'
                      : '#ffebee',
                  color:
                    item.result_name === 'Поверка пройдена'
                      ? '#2e7d32'
                      : '#d32f2f',
                }">
                {{ item.result_name }}
              </span>
              <span v-else>—</span>
            </td>
            <td style="padding: 12px 15px">
              {{ formatDate(item.planned_date_verification) }}
            </td>
            <td style="padding: 12px 15px">
              {{ formatDate(item.real_date_verification) || "—" }}
            </td>
            <td style="padding: 12px 15px">
              {{ item.metrologist_name || "—" }}
            </td>

            <!-- Кнопки действий -->
            <td style="padding: 12px 15px; text-align: center">
              <div style="display: flex; gap: 8px; justify-content: center">
                <!-- Кнопка заполнения данных (только для незавершенных и если пользователь - метролог этой поверки или админ) -->
                <button
                  v-if="!item.is_completed && canEditVerification(item)"
                  @click="openFillDataModal(item)"
                  style="
                    background: none;
                    border: 1px solid #e0e0e0;
                    border-radius: 4px;
                    padding: 4px 8px;
                    cursor: pointer;
                    color: #1976d2;
                  "
                  title="Заполнить данные тестирования">
                  📝 Данные
                </button>

                <!-- Кнопки для админа -->
                <template v-if="userRole === 'Администратор'">
                  <button
                    @click="openEditModal(item)"
                    style="
                      background: none;
                      border: 1px solid #e0e0e0;
                      border-radius: 4px;
                      padding: 4px 8px;
                      cursor: pointer;
                    "
                    title="Редактировать">
                    ✏️ Ред.
                  </button>
                  <button
                    @click="confirmDelete(item)"
                    style="
                      background: none;
                      border: 1px solid #ffcdd2;
                      border-radius: 4px;
                      padding: 4px 8px;
                      cursor: pointer;
                      color: #d32f2f;
                    "
                    title="Удалить">
                    🗑️ Удал.
                  </button>
                </template>
              </div>
            </td>
          </tr>
          <tr v-if="filteredData.length === 0">
            <td
              colspan="9"
              style="padding: 40px; text-align: center; color: #999">
              Нет данных, соответствующих критериям поиска
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно для добавления поверки -->
    <div
      v-if="showAddModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
      "
      @click.self="closeAddModal">
      <div
        style="
          background-color: white;
          border-radius: 12px;
          padding: 25px;
          width: 500px;
          max-width: 90%;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        ">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px">
          Добавить поверку
        </h3>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Средство измерения</label
          >
          <select
            v-model="addForm.id_instrument"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required>
            <option value="">Выберите средство измерения</option>
            <option
              v-for="instrument in instruments"
              :key="instrument.id"
              :value="instrument.id">
              {{ instrument.serial_number }}
            </option>
          </select>
        </div>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Планируемая дата поверки</label
          >
          <input
            v-model="addForm.planned_date_verification"
            type="date"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required />
        </div>

        <div style="margin-bottom: 20px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Дата поступления</label
          >
          <input
            v-model="addForm.date_receipt"
            type="date"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required />
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px">
          <button
            @click="closeAddModal"
            style="
              padding: 10px 20px;
              background-color: white;
              color: black;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            Отмена
          </button>
          <button
            @click="createVerification"
            :disabled="saving"
            style="
              padding: 10px 20px;
              background-color: black;
              color: white;
              border: none;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            {{ saving ? "Сохранение..." : "Создать" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для заполнения данных тестирования -->
    <div
      v-if="showTestDataModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
      "
      @click.self="closeTestDataModal">
      <div
        style="
          background-color: white;
          border-radius: 12px;
          padding: 25px;
          width: 600px;
          max-width: 90%;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        ">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px">
          Данные тестирования
        </h3>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Серийный номер</label
          >
          <input
            :value="testDataForm.serialNumber"
            type="text"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
              background-color: #f5f5f5;
            "
            disabled />
        </div>

        <div
          style="
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
          ">
          <div>
            <label
              style="
                display: block;
                margin-bottom: 5px;
                font-size: 14px;
                color: #333;
              "
            >Температура (°C)</label
            >
            <input
              v-model="testDataForm.temperature"
              type="number"
              step="0.1"
              style="
                width: 100%;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
              "
              required />
          </div>
          <div>
            <label
              style="
                display: block;
                margin-bottom: 5px;
                font-size: 14px;
                color: #333;
              "
            >Давление (мм рт. ст.)</label
            >
            <input
              v-model="testDataForm.pressure"
              type="number"
              step="0.1"
              style="
                width: 100%;
                padding: 10px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
              "
              required />
          </div>
        </div>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Влажность (%)</label
          >
          <input
            v-model="testDataForm.wetness"
            type="number"
            step="0.1"
            min="0"
            max="100"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required />
        </div>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Результаты тестов</label
          >
          <div style="display: flex; gap: 20px; margin-top: 5px">
            <label style="display: flex; align-items: center; gap: 5px">
              <input
                type="checkbox"
                v-model="testDataForm.complete_electric_test" />
              Электрический тест
            </label>
            <label style="display: flex; align-items: center; gap: 5px">
              <input
                type="checkbox"
                v-model="testDataForm.complete_voltage_test" />
              Тест напряжения
            </label>
            <label style="display: flex; align-items: center; gap: 5px">
              <input
                type="checkbox"
                v-model="testDataForm.complete_isolation_test" />
              Тест изоляции
            </label>
          </div>
        </div>

        <div style="margin-bottom: 20px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Использованные эталоны</label
          >
          <select
            v-model="testDataForm.id_reference_devices"
            multiple
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
              min-height: 100px;
            "
            required>
            <option
              v-for="device in referenceDevices"
              :key="device.id"
              :value="device.id">
              {{ device.serial_number }} (валиден до
              {{ formatDate(device.valid_for) }})
            </option>
          </select>
          <small style="color: #666"
          >Удерживайте Ctrl для выбора нескольких</small
          >
        </div>

        <div style="margin-bottom: 20px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Использованные стенды</label
          >
          <select
            v-model="testDataForm.id_test_tools"
            multiple
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
              min-height: 100px;
            "
            required>
            <option v-for="tool in testTools" :key="tool.id" :value="tool.id">
              {{ tool.serial_number }}
              {{ tool.active ? "(активен)" : "(неактивен)" }}
            </option>
          </select>
          <small style="color: #666"
          >Удерживайте Ctrl для выбора нескольких</small
          >
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px">
          <button
            @click="closeTestDataModal"
            style="
              padding: 10px 20px;
              background-color: white;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            Отмена
          </button>
          <button
            @click="saveTestData"
            :disabled="saving"
            style="
              padding: 10px 20px;
              background-color: black;
              color: white;
              border: none;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            {{ saving ? "Сохранение..." : "Сохранить данные" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для завершения поверки -->
    <div
      v-if="showCompleteModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
      "
      @click.self="closeCompleteModal">
      <div
        style="
          background-color: white;
          border-radius: 12px;
          padding: 25px;
          width: 500px;
          max-width: 90%;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        ">
        <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 18px">
          Завершить поверку
        </h3>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Серийный номер</label
          >
          <input
            :value="completeForm.serialNumber"
            type="text"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
              background-color: #f5f5f5;
            "
            disabled />
        </div>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Результат</label
          >
          <select
            v-model="completeForm.id_result"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required>
            <option value="">Выберите результат</option>
            <option
              v-for="result in results"
              :key="result.id"
              :value="result.id">
              {{ result.result_name }}
            </option>
          </select>
        </div>

        <div style="margin-bottom: 15px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Тип поверки</label
          >
          <select
            v-model="completeForm.id_type"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required>
            <option value="">Выберите тип</option>
            <option
              v-for="type in verificationTypes"
              :key="type.id"
              :value="type.id">
              {{ type.type_name }}
            </option>
          </select>
        </div>

        <div style="margin-bottom: 20px">
          <label
            style="
              display: block;
              margin-bottom: 5px;
              font-size: 14px;
              color: #333;
            "
          >Фактическая дата</label
          >
          <input
            v-model="completeForm.real_date_verification"
            type="date"
            style="
              width: 100%;
              padding: 10px;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              font-size: 14px;
            "
            required />
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 10px">
          <button
            @click="closeCompleteModal"
            style="
              padding: 10px 20px;
              background-color: white;
              color: black;
              border: 1px solid #e0e0e0;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            Отмена
          </button>
          <button
            @click="completeVerification"
            :disabled="saving"
            style="
              padding: 10px 20px;
              background-color: black;
              color: white;
              border: none;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">
            {{ saving ? "Сохранение..." : "Завершить" }}
          </button>
        </div>
      </div>
    </div>

    <!-- Диалог подтверждения удаления -->
    <Dialog
      v-model:show="showDeleteDialog"
      title="Подтверждение удаления"
      :message="deleteMessage"
      confirm-text="Удалить"
      @confirm="deleteItem" />

    <!-- Диалог ошибки -->
    <Dialog
      v-model:show="showErrorDialog"
      title="Ошибка"
      :message="errorMessage"
      confirm-text="Понятно"
      @confirm="showErrorDialog = false" />

    <!-- Диалог успеха -->
    <Dialog
      v-model:show="showSuccessDialog"
      title="Успешно"
      :message="successMessage"
      confirm-text="ОК"
      @confirm="showSuccessDialog = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Dialog from '../components/blocks/Dialog.vue';

const router = useRouter();
const API_BASE_URL = 'http://localhost:8000';

// Текущий пользователь
const currentUser = ref(null);

// Роль пользователя
const userRole = ref('Метролог');
const loading = ref(false);
const saving = ref(false);

// Поиск и фильтры
const searchQuery = ref('');
const showFilters = ref(false);
const filters = ref({
  completed: 'all',
  resultId: 'all',
  typeId: 'all',
  plannedFrom: '',
  plannedTo: ''
});

// Диалоги
const showErrorDialog = ref(false);
const showSuccessDialog = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// Данные
const tableData = ref([]);
const instruments = ref([]);
const results = ref([]);
const verificationTypes = ref([]);
const referenceDevices = ref([]);
const testTools = ref([]);

// Модальные окна
const showAddModal = ref(false);
const showTestDataModal = ref(false);
const showCompleteModal = ref(false);
const showEditModal = ref(false);

// Формы
const addForm = ref({
  id_instrument: '',
  planned_date_verification: '',
  date_receipt: ''
});

const testDataForm = ref({
  id: null,
  serialNumber: '',
  temperature: 20,
  pressure: 760,
  wetness: 50,
  complete_electric_test: false,
  complete_voltage_test: false,
  complete_isolation_test: false,
  id_reference_devices: [],
  id_test_tools: []
});

const completeForm = ref({
  id: null,
  serialNumber: '',
  id_result: '',
  id_type: '',
  real_date_verification: ''
});

const editForm = ref({
  id: null,
  instrument_serial: '',
  planned_date_verification: '',
  date_receipt: '',
  id_result: '',
  id_type: ''
});

// Загрузка текущего пользователя
const loadCurrentUser = () => {
  try {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      currentUser.value = JSON.parse(storedUser);
      userRole.value = currentUser.value.admin_role
        ? 'Администратор'
        : 'Метролог';
    }
  } catch {
    // (error)
    // console.error('Error loading current user:', error);
  }
};

// Проверка может ли пользователь редактировать поверку
const canEditVerification = (verification) => {
  if (userRole.value === 'Администратор') return true;
  // Если у поверки нет метролога, то любой может редактировать
  if (!verification.id_metrologist) return true;
  // Если есть метролог, то только он может редактировать
  return (
    currentUser.value && verification.id_metrologist === currentUser.value.id
  );
};

// Проверка может ли пользователь менять статус
const canEditStatus = (verification) => {
  // Статус может менять только админ или метролог этой поверки
  return canEditVerification(verification);
};

// Загрузка справочных данных
const loadResults = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/results/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      results.value = await response.json();
    }
  } catch {
    // console.error('Error loading results:', error);
  }
};

const loadVerificationTypes = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/verification-types/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      verificationTypes.value = await response.json();
    }
  } catch {
    // console.error('Error loading verification types:', error);
  }
};

const loadReferenceDevices = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/reference-devices/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      referenceDevices.value = await response.json();
    }
  } catch {
    // (error)
    // console.error('Error loading reference devices:', error);
  }
};

const loadTestTools = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/test-tools/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      testTools.value = await response.json();
    }
  } catch {
    // (error)
    // console.error('Error loading test tools:', error);
  }
};

const loadInstruments = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch(`${API_BASE_URL}/measurement-instruments/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response.ok) {
      instruments.value = await response.json();
    }
  } catch {
    // (error)
    // console.error('Error loading instruments:', error);
  }
};

// Загрузка поверок
const loadVerifications = async() => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  loading.value = true;
  try {
    let url = `${API_BASE_URL}/verifications/?skip=0&limit=100`;

    if (filters.value.completed === 'completed') {
      url += '&completed=true';
    } else if (filters.value.completed === 'pending') {
      url += '&completed=false';
    }

    if (filters.value.plannedFrom && filters.value.plannedTo) {
      url += `&from_date=${filters.value.plannedFrom}&to_date=${filters.value.plannedTo}`;
    }

    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        router.push('/login');
        return;
      }
      throw new Error('Ошибка загрузки поверок');
    }

    tableData.value = await response.json();
    // console.log('Загружены поверки:', tableData.value);
  } catch (error) {
    // console.error('Error loading verifications:', error);
    errorMessage.value = error.message || 'Ошибка загрузки поверок';
    showErrorDialog.value = true;
  } finally {
    loading.value = false;
  }
};

// Фильтрация данных
const filteredData = computed(() => {
  let data = tableData.value;

  // Поиск по тексту
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    data = data.filter(
      (item) =>
        item.instrument_serial?.toLowerCase().includes(query) ||
        item.type_name?.toLowerCase().includes(query) ||
        item.result_name?.toLowerCase().includes(query)
    );
  }

  // Фильтр по результату
  if (filters.value.resultId !== 'all') {
    data = data.filter((item) => item.id_result == filters.value.resultId);
  }

  // Фильтр по типу поверки
  if (filters.value.typeId !== 'all') {
    data = data.filter((item) => item.id_type == filters.value.typeId);
  }

  return data;
});

// Применить фильтры
const applyFilters = () => {
  showFilters.value = false;
  loadVerifications();
};

// Сбросить фильтры
const resetFilters = () => {
  filters.value = {
    completed: 'all',
    resultId: 'all',
    typeId: 'all',
    plannedFrom: '',
    plannedTo: ''
  };
  loadVerifications();
};

// Форматирование даты
const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU');
};

// Обновление статуса
const updateStatus = async(item) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  try {
    // Если статус меняется на "Завершена", открываем модальное окно завершения
    if (item.is_completed) {
      openCompleteModal(item);
    } else {
      // Если статус меняется на "В процессе", просто обновляем через API
      const response = await fetch(`${API_BASE_URL}/verifications/${item.id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          real_date_verification: null
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Ошибка при обновлении статуса');
      }

      successMessage.value = 'Статус обновлен';
      showSuccessDialog.value = true;
      loadVerifications();
    }
  } catch (error) {
    // console.error('Error updating status:', error);
    errorMessage.value = error.message || 'Ошибка при обновлении статуса';
    showErrorDialog.value = true;
    // Возвращаем старое значение
    item.is_completed = !item.is_completed;
  }
};

// Добавление поверки
const openAddModal = () => {
  addForm.value = {
    id_instrument: '',
    planned_date_verification: '',
    date_receipt: ''
  };
  loadInstruments();
  showAddModal.value = true;
};

const closeAddModal = () => {
  showAddModal.value = false;
};

const createVerification = async() => {
  if (
    !addForm.value.id_instrument ||
    !addForm.value.planned_date_verification ||
    !addForm.value.date_receipt
  ) {
    errorMessage.value = 'Заполните все поля';
    showErrorDialog.value = true;
    return;
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  saving.value = true;
  try {
    const response = await fetch(`${API_BASE_URL}/verifications/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(addForm.value)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при создании поверки');
    }

    successMessage.value = 'Поверка успешно создана';
    showSuccessDialog.value = true;
    closeAddModal();
    loadVerifications();
  } catch (error) {
    // console.error('Error creating verification:', error);
    errorMessage.value = error.message || 'Ошибка при создании поверки';
    showErrorDialog.value = true;
  } finally {
    saving.value = false;
  }
};

// Заполнение данных тестирования
const openFillDataModal = (item) => {
  if (!canEditVerification(item)) {
    errorMessage.value = 'У вас нет прав для редактирования этой поверки';
    showErrorDialog.value = true;
    return;
  }

  testDataForm.value = {
    id: item.id,
    serialNumber: item.instrument_serial,
    temperature: 20,
    pressure: 760,
    wetness: 50,
    complete_electric_test: false,
    complete_voltage_test: false,
    complete_isolation_test: false,
    id_reference_devices: [],
    id_test_tools: []
  };
  loadReferenceDevices();
  loadTestTools();
  showTestDataModal.value = true;
};

const closeTestDataModal = () => {
  showTestDataModal.value = false;
};

const saveTestData = async() => {
  if (
    !testDataForm.value.temperature ||
    !testDataForm.value.pressure ||
    !testDataForm.value.wetness
  ) {
    errorMessage.value = 'Заполните все параметры окружающей среды';
    showErrorDialog.value = true;
    return;
  }

  if (testDataForm.value.id_reference_devices.length === 0) {
    errorMessage.value = 'Выберите хотя бы один эталон';
    showErrorDialog.value = true;
    return;
  }

  if (testDataForm.value.id_test_tools.length === 0) {
    errorMessage.value = 'Выберите хотя бы один стенд';
    showErrorDialog.value = true;
    return;
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  saving.value = true;
  try {
    const response = await fetch(
      `${API_BASE_URL}/verifications/${testDataForm.value.id}/test-data`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          temperature: parseFloat(testDataForm.value.temperature),
          pressure: parseFloat(testDataForm.value.pressure),
          wetness: parseFloat(testDataForm.value.wetness),
          complete_electric_test: testDataForm.value.complete_electric_test,
          complete_voltage_test: testDataForm.value.complete_voltage_test,
          complete_isolation_test: testDataForm.value.complete_isolation_test,
          id_reference_devices: testDataForm.value.id_reference_devices,
          id_test_tools: testDataForm.value.id_test_tools
        })
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при сохранении данных');
    }

    successMessage.value = 'Данные тестирования сохранены';
    showSuccessDialog.value = true;
    closeTestDataModal();
  } catch (error) {
    // console.error('Error saving test data:', error);
    errorMessage.value = error.message || 'Ошибка при сохранении данных';
    showErrorDialog.value = true;
  } finally {
    saving.value = false;
  }
};

// Завершение поверки
const openCompleteModal = (item) => {
  completeForm.value = {
    id: item.id,
    serialNumber: item.instrument_serial,
    id_result: '',
    id_type: '',
    real_date_verification: new Date().toISOString().split('T')[0]
  };
  showCompleteModal.value = true;
};

const closeCompleteModal = () => {
  showCompleteModal.value = false;
};

const completeVerification = async() => {
  if (
    !completeForm.value.id_result ||
    !completeForm.value.id_type ||
    !completeForm.value.real_date_verification
  ) {
    errorMessage.value = 'Заполните все поля';
    showErrorDialog.value = true;
    return;
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  saving.value = true;
  try {
    const response = await fetch(
      `${API_BASE_URL}/verifications/${completeForm.value.id}/complete`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          id_result: parseInt(completeForm.value.id_result),
          id_type: parseInt(completeForm.value.id_type),
          real_date_verification: completeForm.value.real_date_verification
        })
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при завершении поверки');
    }

    successMessage.value = 'Поверка успешно завершена';
    showSuccessDialog.value = true;
    closeCompleteModal();
    loadVerifications();
  } catch (error) {
    // console.error('Error completing verification:', error);
    errorMessage.value = error.message || 'Ошибка при завершении поверки';
    showErrorDialog.value = true;
  } finally {
    saving.value = false;
  }
};

// Редактирование поверки
const openEditModal = (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для редактирования';
    showErrorDialog.value = true;
    return;
  }

  editForm.value = {
    id: item.id,
    instrument_serial: item.instrument_serial,
    planned_date_verification: item.planned_date_verification || '',
    date_receipt: item.date_receipt || '',
    id_result: item.id_result || '',
    id_type: item.id_type || ''
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
};

// eslint-disable-next-line
const updateVerification = async () => {
  if (!editForm.value.planned_date_verification) {
    errorMessage.value = 'Заполните планируемую дату';
    showErrorDialog.value = true;
    return;
  }

  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  saving.value = true;
  try {
    const updateData = {
      planned_date_verification: editForm.value.planned_date_verification
    };

    if (editForm.value.date_receipt) {
      updateData.date_receipt = editForm.value.date_receipt;
    }
    if (editForm.value.id_result) {
      updateData.id_result = parseInt(editForm.value.id_result);
    }
    if (editForm.value.id_type) {
      updateData.id_type = parseInt(editForm.value.id_type);
    }

    const response = await fetch(
      `${API_BASE_URL}/verifications/${editForm.value.id}`,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при обновлении поверки');
    }

    successMessage.value = 'Поверка успешно обновлена';
    showSuccessDialog.value = true;
    closeEditModal();
    loadVerifications();
  } catch (error) {
    // console.error('Error updating verification:', error);
    errorMessage.value = error.message || 'Ошибка при обновлении поверки';
    showErrorDialog.value = true;
  } finally {
    saving.value = false;
  }
};

// Удаление поверки
const showDeleteDialog = ref(false);
const itemToDelete = ref(null);

const confirmDelete = (item) => {
  if (userRole.value !== 'Администратор') {
    errorMessage.value = 'У вас нет прав для удаления';
    showErrorDialog.value = true;
    return;
  }
  itemToDelete.value = item;
  showDeleteDialog.value = true;
};

const deleteMessage = computed(() => {
  return `Вы уверены, что хотите удалить поверку #${itemToDelete.value?.id} для прибора ${itemToDelete.value?.instrument_serial}?`;
});

const deleteItem = async() => {
  if (!itemToDelete.value) return;

  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/verifications/${itemToDelete.value.id}`,
      {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Ошибка при удалении поверки');
    }

    successMessage.value = 'Поверка успешно удалена';
    showSuccessDialog.value = true;
    loadVerifications();
  } catch (error) {
    // console.error('Error deleting verification:', error);
    errorMessage.value = error.message || 'Ошибка при удалении поверки';
    showErrorDialog.value = true;
  } finally {
    showDeleteDialog.value = false;
    itemToDelete.value = null;
  }
};

// Инициализация
onMounted(() => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    router.push('/login');
    return;
  }
  loadCurrentUser();
  loadResults();
  loadVerificationTypes();
  loadVerifications();
});
</script>
