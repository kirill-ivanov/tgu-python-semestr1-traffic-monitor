<script setup>
import {ref} from 'vue'
import {reactive} from 'vue'
import moment from "moment";

const isLoading = ref(false);
const tableData = reactive({
  arr: []
})

const formModel = reactive({
  dateFrom: new Date(),
  dateTo: new Date(),
  group: 'no',
})

const currentGroup = ref('')
const dateFormatter = (row) => {
  if (currentGroup.value === 'hour') {
    return moment(row.dt).format('YYYY-MM-DD HH')
  } else if (currentGroup.value === 'day') {
    return moment(row.dt).format('YYYY-MM-DD')
  } else {
    return moment(row.dt).format('YYYY-MM-DD HH:mm:ss')
  }
}

const onSubmit = async () => {
  isLoading.value = true;
  currentGroup.value = formModel.group;
  try {
    const params = new URLSearchParams({
      date_from: moment(formModel.dateFrom).format("DD.MM.YYYY"),
      date_to: moment(formModel.dateTo).format("DD.MM.YYYY"),
      group: formModel.group
    }).toString();
    fetch(`http://localhost:8000/api/stat?${params}`)
        .then(res => res.json())
        .then(data => tableData.arr = data.result);
  } catch (e) {
    console.log(e)
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div>
    <h1>Статистика определения объектов</h1>

    <el-form inline>
      <el-form-item label="Дата с">
        <el-date-picker
            v-model="formModel.dateFrom"
            type="date"
            size="small"
            style="width: 100px"
            format="DD.MM.YYYY"
        />
      </el-form-item>
      <el-form-item label="по">
        <el-date-picker
            v-model="formModel.dateTo"
            type="date"
            size="small"
            style="width: 100px"
            format="DD.MM.YYYY"
        />
      </el-form-item>
      <el-form-item label="Группировка">
        <el-select
            v-model="formModel.group"
            size="small"
            style="width: 100px"
        >
          <el-option key="no" label="нет" value="no"/>
          <el-option key="day" label="по дням" value="day"/>
          <el-option key="hour" label="по часам" value="hour"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button size="small" type="primary" @click="onSubmit">Поиск</el-button>
      </el-form-item>
    </el-form>
    <el-table
        :data="tableData.arr" empty-text="Данных нет"
        v-loading="isLoading"
        element-loading-text="Идет загрузка ..."
    >
      <el-table-column prop="dt" label="Дата" width="250" :formatter="dateFormatter"/>
      <el-table-column prop="type" label="Тип" width="180"/>
      <el-table-column prop="count" label="Количество" width="250"/>
    </el-table>
  </div>
</template>