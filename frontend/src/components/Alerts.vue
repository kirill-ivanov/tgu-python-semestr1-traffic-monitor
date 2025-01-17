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
  type: 'all',
})

const dateFormatter = (row) => {
  return moment(row.dt).format('YYYY-MM-DD HH:mm:ss')
}

const onSubmit = async () => {
  isLoading.value = true;
  try {
    const params = new URLSearchParams({
      date_from: moment(formModel.dateFrom).format("DD.MM.YYYY"),
      date_to: moment(formModel.dateTo).format("DD.MM.YYYY"),
      type: formModel.type
    }).toString();
    fetch(`http://localhost:8000/api/alert?${params}`)
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
    <h1>Уведомления</h1>

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
      <el-form-item label="Тип уведомления">
        <el-select
            v-model="formModel.type"
            size="small"
            style="width: 150px"
        >
          <el-option key="all" label="Все" value="all"/>
          <el-option key="warning" label="Только предупреждения" value="WARNING"/>
          <el-option key="error" label="Только ошибки" value="ERROR"/>
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
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="dt" label="Дата" width="250" :formatter="dateFormatter"/>
      <el-table-column prop="type" label="Тип" width="180"/>
      <el-table-column prop="message" label="Сообщение" width="250"/>
    </el-table>
  </div>
</template>