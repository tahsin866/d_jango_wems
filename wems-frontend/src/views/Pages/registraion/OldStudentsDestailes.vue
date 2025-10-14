<template>
  <div
  style="font-family: 'SolaimanLipi', sans-serif;"
  class="bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="mx-auto">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center min-h-screen">
        <div class="text-center">
          <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="8" fill="var(--surface-ground)" animationDuration=".5s" />
          <p class="mt-4 text-gray-600">Loading student information...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error">
        <Message severity="error" :closable="false">
          <div class="flex items-center">
            <div>
              <h3 class="text-md font-semibold text-red-800">Error loading student data</h3>
              <p class="mt-1 text-md text-red-700">{{ error }}</p>
              <Button @click="fetchStudentData(route.params.id)" label="Try again" class="p-button-text p-button-danger" />
            </div>
          </div>
        </Message>
      </div>

      <!-- Student Data -->
      <div v-else>
        <Card>
          <template #header>
            <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-6 py-4">
              <div class="flex items-center justify-between">
                <h1 class="text-2xl font-bold text-white">ছাত্রদের তথ্য</h1>
                <div class="flex items-center space-x-2">
                  <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {{ studentData.status || 'Active' }}
                  </span>
                  <span v-if="studentData.is_old" class="bg-amber-100 text-amber-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    পুরাতন ছাত্র
                  </span>
                </div>
              </div>
            </div>
          </template>

          <template #content>
            <!-- Student Photo and Basic Info -->
            <div class="p-6 border-b border-gray-200">
              <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6">
                <!-- Student Photo -->
                <div class="flex-shrink-0">
                  <Image
                    :src="studentData.photo || '/placeholder-avatar.png'"
                    alt="Student Photo"
                    width="150"
                    height="150"
                    class="rounded-full border-4 border-gray-200"
                    preview
                  />
                </div>

                <!-- Basic Information -->
                <div class="flex-1 text-center sm:text-left">
                  <div class="flex items-center gap-2 justify-center sm:justify-start">
                    <h2 v-if="!editingFields.student_name_bn" class="text-2xl font-bold text-gray-900">{{ studentData.student_name_bn }}</h2>
                    <InputText
                      v-else
                      v-model="studentData.student_name_bn"
                      type="text"
                      class="text-2xl font-bold"
                    />
                    <Button @click="toggleEdit('student_name_bn')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                  </div>
                  <div class="flex items-center gap-2 justify-center sm:justify-start">
                    <h3 v-if="!editingFields.student_name_en" class="text-lg text-gray-600">{{ studentData.student_name_en }}</h3>
                    <InputText
                      v-else
                      v-model="studentData.student_name_en"
                      type="text"
                      class="text-lg"
                    />
                    <Button @click="toggleEdit('student_name_en')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                  </div>
                  <div class="flex items-center gap-2 justify-center sm:justify-start">
                    <h4 v-if="!editingFields.student_name_ar" class="text-lg text-gray-600" dir="rtl">{{ studentData.student_name_ar }}</h4>
                    <InputText
                      v-else
                      v-model="studentData.student_name_ar"
                      type="text"
                      class="text-lg"
                      dir="rtl"
                    />
                    <Button @click="toggleEdit('student_name_ar')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                  </div>

                  <div class="mt-3 flex flex-wrap justify-center sm:justify-start gap-2">
                    <div class="flex items-center gap-1">
                      <Badge :value="`রোন নম্বর:`" class="p-badge-info" />
                      <span v-if="!editingFields.roll_no" class="text-sm text-gray-900">{{ studentData.roll_no }}</span>
                      <InputNumber
                        v-else
                        v-model="studentData.roll_no"
                        class="text-sm w-20"
                      />
                      <Button @click="toggleEdit('roll_no')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-xs" />
                    </div>
                    <Badge :value="`রেজিস্ট্রেশন নম্বর: ${studentData.reg_no}`" class="p-badge-success" />
                    <div class="flex items-center gap-1">
                      <Badge :value="`শিক্ষাবর্ষ:`" class="p-badge-secondary" />
                      <span v-if="!editingFields.year" class="text-sm text-gray-900">{{ studentData.year }}</span>
                      <InputNumber
                        v-else
                        v-model="studentData.year"
                        class="text-sm w-20"
                      />
                      <Button @click="toggleEdit('year')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-xs" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Detailed Information Tabs -->
            <div class="bg-white">
              <TabView v-model:activeIndex="activeTabIndex">
                <TabPanel header="ব্যক্তিগত তথ্য">
                  <div class="space-y-6">
                    <h3 class="text-lg font-semibold text-gray-900">ব্যক্তিগত তথ্য</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <Fieldset legend="ছাত্রের তথ্য">
                          <div class="mt-2 space-y-2">
                            <div class="flex justify-between items-center">
                              <label class="text-md text-gray-600">জন্ম-তারিখ:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.date_of_birth" class="text-md text-gray-900">{{ formatDate(studentData.date_of_birth) }}</span>
                                <Calendar
                                  v-else
                                  v-model="studentData.date_of_birth"
                                  dateFormat="yy-mm-dd"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('date_of_birth')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">মোবাইল:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.mobile" class="text-md text-gray-900">{{ studentData.mobile }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.mobile"
                                  type="tel"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('mobile')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">পরীক্ষার্থীর ধরণ:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.students_type" class="text-md text-gray-900">{{ studentData.students_type }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.students_type"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('students_type')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <div>
                        <Fieldset legend="পিতার ইনফরমেশন">
                          <div class="mt-2 space-y-2">
                            <div>
                              <label class="text-md font-semibold text-gray-600">পিতার নাম (বাংলা):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.father_name_bn" class="text-md text-gray-900">{{ studentData.father_name_bn }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.father_name_bn"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('father_name_bn')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div>
                              <label class="text-md font-semibold text-gray-600">পিতার নাম (ইংরেজি):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.father_name_en" class="text-md text-gray-900">{{ studentData.father_name_en }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.father_name_en"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('father_name_en')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div>
                              <label class="text-md font-semibold text-gray-600">পিতার নাম (আরবি):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.father_name_ar" class="text-md text-gray-900" dir="rtl">{{ studentData.father_name_ar }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.father_name_ar"
                                  type="text"
                                  class="text-md"
                                  dir="rtl"
                                />
                                <Button @click="toggleEdit('father_name_ar')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <div>
                        <Fieldset legend="মাতার ইনফরমেশন">
                          <div class="mt-2 space-y-2">
                            <div>
                              <label class="text-md font-semibold text-gray-600">মাতার নাম (বাংলা):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.mother_name_bn" class="text-md text-gray-900">{{ studentData.mother_name_bn }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.mother_name_bn"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('mother_name_bn')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div>
                              <label class="text-md font-semibold text-gray-600">মাতার নাম (ইংরেজি):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.mother_name_en" class="text-md text-gray-900">{{ studentData.mother_name_en }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.mother_name_en"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('mother_name_en')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div>
                              <label class="text-md font-semibold text-gray-600">মাতার নাম (আরবি):</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.mother_name_ar" class="text-md text-gray-900" dir="rtl">{{ studentData.mother_name_ar }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.mother_name_ar"
                                  type="text"
                                  class="text-md"
                                  dir="rtl"
                                />
                                <Button @click="toggleEdit('mother_name_ar')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <div>
                        <Fieldset legend="সিস্টেম ইনফরমেশন">
                          <div class="mt-2 space-y-2">
                            <div class="flex justify-between">
                              <label class="text-md font-semibold text-gray-600">আইপি এড্রেস:</label>
                              <div class="text-md text-gray-900">{{ studentData.ip_address }}</div>
                            </div>
                            <div class="flex justify-between">
                              <label class="text-md font-semibold text-gray-600">Created:</label>
                              <div class="text-md text-gray-900">{{ formatDateTime(studentData.created_at) }}</div>
                            </div>
                            <div class="flex justify-between">
                              <label class="text-md font-semibold text-gray-600">Updated:</label>
                              <div class="text-md text-gray-900">{{ formatDateTime(studentData.updated_at) }}</div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>
                    </div>
                  </div>
                </TabPanel>

                <TabPanel header="শিক্ষাগত তথ্য">
                  <div class="space-y-6">
                    <h3 class="text-lg font-semibold text-gray-900">শিক্ষাগত তথ্য</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <Fieldset legend="নিবন্ধন তথ্য">
                          <div class="mt-2 space-y-2">
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">মারহালা:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.marhala_id" class="text-md text-gray-900">{{ getMarhalaName(studentData.marhala_id) }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.marhala_id"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('marhala_id')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">শিক্ষার্থীর ধরণ:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.srtype" class="text-md text-gray-900">{{ getStudentTypeDisplay(studentData.srtype) }}</span>
                                <InputText
                                  v-else
                                  v-model="studentData.srtype"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('srtype')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">কেন্দ্রীয় পরীক্ষা:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.exam_id" class="text-md text-gray-900">{{ getExamName(studentData.exam_id) }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.exam_id"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('exam_id')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <div>
                        <Fieldset legend="মাদরসার তথ্য">
                          <div class="mt-2 space-y-2">
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">মাদরাসার নাম:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.madrasha_id" class="text-md text-gray-900">{{ getMadrashaName(studentData.madrasha_id) }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.madrasha_id"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('madrasha_id')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">মারকাযের নাম:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.markaz_id" class="text-md text-gray-900">{{ getMarkazName(studentData.markaz_id) }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.markaz_id"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('markaz_id')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">হিজরি সাল:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.hijri_year" class="text-md text-gray-900">{{ studentData.hijri_year }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.hijri_year"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('hijri_year')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">বাংলা সাল:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.bangla_year" class="text-md text-gray-900">{{ studentData.bangla_year }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.bangla_year"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('bangla_year')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <div>
                        <Fieldset legend="শিক্ষাগত অবস্থা">
                          <div class="mt-2 space-y-2">
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">নিবন্ধন অবস্থা:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.status" class="text-md text-gray-900">{{ studentData.status }}</span>
                                <Dropdown
                                  v-else
                                  v-model="studentData.status"
                                  :options="['pending', 'approved', 'submitted', 'returned']"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('status')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">পুরাতন ছাত্র:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.is_old" class="text-md text-gray-900">{{ studentData.is_old ? 'Yes' : 'No' }}</span>
                                <Dropdown
                                  v-else
                                  v-model="studentData.is_old"
                                  :options="[{label: 'No', value: 0}, {label: 'Yes', value: 1}]"
                                  optionLabel="label"
                                  optionValue="value"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('is_old')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                            <div class="flex justify-between items-center">
                              <label class="text-md font-semibold text-gray-600">অনিয়মিত এর সাবজেক্ট:</label>
                              <div class="flex items-center gap-2">
                                <span v-if="!editingFields.irregular_sub" class="text-md text-gray-900">{{ studentData.irregular_sub }}</span>
                                <InputNumber
                                  v-else
                                  v-model="studentData.irregular_sub"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('irregular_sub')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>
                    </div>
                  </div>
                </TabPanel>

                <TabPanel header="ঠিকানা এবং সংযুক্তি">
                  <div class="space-y-6">
                    <h3 class="text-lg font-semibold text-gray-900">ঠিকানা এবং সংযুক্তি</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <!-- Address Information -->
                      <div>
                        <Fieldset legend="ঠিকানা" :pt="{
                          legend: { className: 'text-xl font-bold text-white bg-gradient-to-r from-gray-700 to-gray-600 px-6 py-4 rounded-t' },
                          content: { className: 'p-6 bg-gray-50 overflow-visible' }
                        }">
                          <template #legend>
                            <div class="flex gap-4 items-center">
                              <div class="p-2 rounded-sm bg-white bg-opacity-20 backdrop-blur-sm">
                                <i class="text-2xl text-white fa-home"></i>
                              </div>
                              <span class="text-white text-xl font-bold tracking-wide">ঠিকানা</span>
                            </div>
                          </template>

                          <div class="grid grid-cols-1 gap-6 overflow-visible">
                            <!-- বিভাগ -->
                            <div>
                              <label for="division" class="block text-base font-medium text-gray-700 mb-2">বিভাগ</label>
                              <Dropdown
                                id="division"
                                v-model="localAddress.division"
                                :options="divisions"
                                optionLabel="Division"
                                optionValue="id"
                                placeholder="সকল বিভাগ"
                                :disabled="addressLoading.divisions"
                                :loading="addressLoading.divisions"
                                class="w-full"
                                :pt="{
                                  root: { class: 'w-full' },
                                  input: { class: 'w-full bg-gray-50 border-gray-300' },
                                  list: { class: 'z-50' }
                                }"
                                @change="onDivisionChange"
                              />
                              <small v-if="addressLoading.divisions" class="text-md text-gray-500 block mt-1">Loading divisions...</small>
                            </div>

                            <!-- জেলা -->
                            <div>
                              <label for="district" class="block text-base font-medium text-gray-700 mb-2">জেলা</label>
                              <Dropdown
                                id="district"
                                v-model="localAddress.district"
                                :options="districts"
                                optionLabel="District"
                                optionValue="DesID"
                                placeholder="সকল জেলা"
                                :disabled="addressLoading.districts || (!localAddress.division && divisions.length > 0)"
                                :loading="addressLoading.districts"
                                class="w-full"
                                :pt="{
                                  root: { class: 'w-full' },
                                  input: { class: 'w-full bg-gray-50 border-gray-300' },
                                  list: { class: 'z-50' }
                                }"
                                @change="onDistrictChange"
                              />
                              <small v-if="addressLoading.districts" class="text-md text-gray-500 block mt-1">Loading districts...</small>
                              <small v-else-if="!localAddress.division && divisions.length > 0" class="text-md text-gray-500 block mt-1">বিভাগ নির্বাচন করুন</small>
                            </div>

                            <!-- থানা/উপজিলা -->
                            <div>
                              <label for="thana" class="block text-base font-medium text-gray-700 mb-2">থানা/উপজিলা</label>
                              <Dropdown
                                id="thana"
                                v-model="localAddress.Thana"
                                :options="thanas"
                                optionLabel="Thana"
                                optionValue="Thana_ID"
                                placeholder="সকল থানা"
                                :disabled="addressLoading.thanas || (!localAddress.district && districts.length > 0)"
                                :loading="addressLoading.thanas"
                                class="w-full"
                                :pt="{
                                  root: { class: 'w-full' },
                                  input: { class: 'w-full bg-gray-50 border-gray-300' },
                                  list: { class: 'z-50' }
                                }"
                                @change="onThanaChange"
                              />
                              <small v-if="addressLoading.thanas" class="text-md text-gray-500 block mt-1">Loading thanas...</small>
                              <small v-else-if="!localAddress.district && districts.length > 0" class="text-md text-gray-500 block mt-1">জেলা নির্বাচন করুন</small>
                            </div>
                          </div>
                        </Fieldset>
                      </div>

                      <!-- Document Information -->
                      <div>
                        <Fieldset legend="ডকুমেন্টস এবং ছবি">
                          <div class="mt-2 space-y-4">
                            <!-- Passport -->
                            <div>
                              <label class="text-md font-semibold text-gray-600">পাসপোর্ট ছবি:</label>
                              <div class="mt-1">
                                <Image
                                  v-if="studentAddressData.passport_photo"
                                  :src="studentAddressData.passport_photo"
                                  alt="Passport Photo"
                                  width="100"
                                  height="100"
                                  class="rounded-lg border border-gray-300"
                                  preview
                                />
                                <span v-else class="text-md text-gray-500">No photo available</span>
                              </div>
                            </div>

                            <!-- Birth Certificate -->
                            <div>
                              <label class="text-md font-semibold text-gray-600">জন্ম নিবন্ধন নং:</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.birth_certificate_no" class="text-md text-gray-900">{{ studentAddressData.birth_certificate_no || 'N/A' }}</span>
                                <InputText
                                  v-else
                                  v-model="studentAddressData.birth_certificate_no"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('birth_certificate_no')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                              <label class="text-md font-semibold text-gray-600 mt-2">জন্ম নিবন্ধন ছবি:</label>
                              <div class="mt-1">
                                <Image
                                  v-if="studentAddressData.birth_certificate_photo"
                                  :src="studentAddressData.birth_certificate_photo"
                                  alt="Birth Certificate"
                                  width="100"
                                  height="100"
                                  class="rounded-lg border border-gray-300"
                                  preview
                                />
                                <span v-else class="text-md text-gray-500">No photo available</span>
                              </div>
                            </div>

                            <!-- NID -->
                            <div>
                              <label class="text-md font-semibold text-gray-600">জাতিয় পরিচয়পত্র তথ্য:</label>
                              <div class="flex items-center gap-2 mt-1">
                                <span v-if="!editingFields.nid_no" class="text-md text-gray-900">{{ studentAddressData.nid_no || 'N/A' }}</span>
                                <InputText
                                  v-else
                                  v-model="studentAddressData.nid_no"
                                  type="text"
                                  class="text-md"
                                />
                                <Button @click="toggleEdit('nid_no')" icon="pi pi-pencil" class="p-button-rounded p-button-text p-button-sm" />
                              </div>
                              <label class="text-md font-semibold text-gray-600 mt-2">জাতীয় পরিচয়পত্রের ছবি:</label>
                              <div class="mt-1">
                                <Image
                                  v-if="studentAddressData.nid_photo"
                                  :src="studentAddressData.nid_photo"
                                  alt="NID Photo"
                                  width="100"
                                  height="100"
                                  class="rounded-lg border border-gray-300"
                                  preview
                                />
                                <span v-else class="text-md text-gray-500">No photo available</span>
                              </div>
                            </div>
                          </div>
                        </Fieldset>
                      </div>
                    </div>
                  </div>
                </TabPanel>

                <TabPanel header="একশন">
                  <div class="space-y-6">
                    <h3 class="text-lg font-semibold text-gray-900">একশন</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Button @click="editStudent" label="Edit Student" icon="pi pi-pencil" class="p-button-info" />
                      <Button @click="downloadPDF" label="Download PDF" icon="pi pi-download" class="p-button-secondary" />
                      <Button @click="printCertificate" label="Print Certificate" icon="pi pi-print" class="p-button-secondary" />
                      <Button @click="deleteRecord" label="Delete Record" icon="pi pi-trash" class="p-button-danger" />
                    </div>
                  </div>
                </TabPanel>
              </TabView>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { StudentService } from '@/services/studentService'

// PrimeVue imports
import Card from 'primevue/card'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Calendar from 'primevue/calendar'
import Image from 'primevue/image'
import Badge from 'primevue/badge'
import Fieldset from 'primevue/fieldset'
import ProgressSpinner from 'primevue/progressspinner'
import Message from 'primevue/message'
import Dropdown from 'primevue/dropdown'

// Reactive state
const route = useRoute()
const activeTab = ref('personal')
const activeTabIndex = computed(() => {
  const tabMap = {
    'personal': 0,
    'academic': 1,
    'address': 2,
    'actions': 3
  }
  return tabMap[activeTab.value] || 0
})

const loading = ref(true)
const error = ref(null)

const tabs = ref([
  { id: 'personal', name: 'ব্যক্তিগত তথ্য' },
  { id: 'academic', name: 'শিক্ষাগত তথ্য' },
  { id: 'address', name: 'ঠিকানা এবং সংযুক্তি' },
  { id: 'actions', name: ' একশন' }
])

// Student data as reactive object
const studentData = reactive({})

// Student Address data as reactive object
const studentAddressData = reactive({})

// Editing state - track which fields are being edited
const editingFields = reactive({})
const editingAddressFields = reactive({})

// Address Data
const divisions = ref([])
const districts = ref([])
const thanas = ref([])

const localAddress = reactive({
  division: '',
  district: '',
  Thana: ''
})

const addressLoading = computed(() => ({
  divisions: false,
  districts: false,
  thanas: false
}))

// Store original values for cancel functionality
const originalValues = reactive({})

// Methods
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

// Data mapping methods
const getMarhalaName = (marhalaId) => {
  if (!marhalaId) return 'N/A'

  // Use the current_class field from the API response (mapped from backend)
  if (studentData.current_class) {
    return studentData.current_class
  }

  // Fallback mapping for common marhalas
  const marhalaMapping = {
    1: 'ইবতেদাইয়্যাহ',
    2: 'মুতাওয়াসসিতা',
    3: 'সানাবিয়া',
    4: 'সানাবিয়া উলইয়া',
    5: 'ফযীলত',
    6: 'হিফজুল কোরান',
    7: 'কিরাআত',
  }
  return marhalaMapping[marhalaId] || `মারহালা ${marhalaId}`
}

const getStudentTypeDisplay = (studentType) => {
  if (studentType === 0 || studentType === '0') {
    return 'Female (ছাত্রী)'
  } else if (studentType === 1 || studentType === '1') {
    return 'Male (ছাত্র)'
  }
  return studentType || 'N/A'
}

const getExamName = (examId) => {
  if (!examId) return 'N/A'

  // Use the exam_name_Bn field from the API response (mapped from backend)
  if (studentData.exam_name_Bn) {
    return studentData.exam_name_Bn
  }

  return `পরীক্ষা ${examId}`
}

const getMadrashaName = (madrashaId) => {
  if (!madrashaId) return 'N/A'

  // Use the current_madrasha field from the API response (mapped from backend)
  if (studentData.current_madrasha) {
    return studentData.current_madrasha
  }

  return `মাদরাসা ${madrashaId}`
}

const getMarkazName = (markazId) => {
  if (!markazId) return 'N/A'

  // Use the current_markaz field from the API response (mapped from backend)
  if (studentData.current_markaz) {
    return studentData.current_markaz
  }

  return `মারকাজ ${markazId}`
}

const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return 'N/A'
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(dateTimeString).toLocaleString(undefined, options)
}

// Edit methods
const toggleEdit = (fieldName) => {
  const isAddressField = ['division', 'district', 'thana'].includes(fieldName)

  if (isAddressField) {
    if (editingAddressFields[fieldName]) {
      // Save the changes
      saveAddressField(fieldName)
    } else {
      // Start editing
      originalValues[fieldName] = studentAddressData[fieldName]
      editingAddressFields[fieldName] = true
    }
  } else {
    if (editingFields[fieldName]) {
      // Save the changes
      saveField(fieldName)
    } else {
      // Start editing
      originalValues[fieldName] = studentData[fieldName]
      editingFields[fieldName] = true
    }
  }
}

const saveField = async (fieldName) => {
  try {
    loading.value = true

    const userId = localStorage.getItem('user_id') || null
    const updateData = { [fieldName]: studentData[fieldName] }
    const params = { user_id: userId }

    const response = await StudentService.updateStudentField(studentData.id, updateData, params)

    if (response.success) {
      editingFields[fieldName] = false
      delete originalValues[fieldName]

      // Show success message
      showSuccessMessage('Field updated successfully')
    } else {
      // Revert to original value on error
      studentData[fieldName] = originalValues[fieldName]
      editingFields[fieldName] = false
      delete originalValues[fieldName]

      error.value = response.error || 'Failed to update field'
    }
  } catch (err) {
    console.error('Error updating field:', err)
    // Revert to original value on error
    studentData[fieldName] = originalValues[fieldName]
    editingFields[fieldName] = false
    delete originalValues[fieldName]

    error.value = err.message || 'Failed to update field'
  } finally {
    loading.value = false
  }
}

const saveAddressField = async (fieldName) => {
  try {
    loading.value = true

    const userId = localStorage.getItem('user_id') || null
    const updateData = { [fieldName]: studentAddressData[fieldName] }
    const params = { user_id: userId }

    const response = await StudentService.updateStudentAddressField(studentData.id, updateData, params)

    if (response.success) {
      editingAddressFields[fieldName] = false
      delete originalValues[fieldName]

      // Show success message
      showSuccessMessage('Address field updated successfully')
    } else {
      // Revert to original value on error
      studentAddressData[fieldName] = originalValues[fieldName]
      editingAddressFields[fieldName] = false
      delete originalValues[fieldName]

      error.value = response.error || 'Failed to update address field'
    }
  } catch (err) {
    console.error('Error updating address field:', err)
    // Revert to original value on error
    studentAddressData[fieldName] = originalValues[fieldName]
    editingAddressFields[fieldName] = false
    delete originalValues[fieldName]

    error.value = err.message || 'Failed to update address field'
  } finally {
    loading.value = false
  }
}

const showSuccessMessage = (message) => {
  // Simple success notification - you can enhance this with a toast library
  const notification = document.createElement('div')
  notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50'
  notification.textContent = message
  document.body.appendChild(notification)

  setTimeout(() => {
    document.body.removeChild(notification)
  }, 3000)
}

// Action methods
const editStudent = () => {
  console.log('Edit student:', studentData.id)
  // Navigate to edit page or open modal
}

const downloadPDF = () => {
  console.log('Download PDF for student:', studentData.id)
  // Implement PDF download logic
}

const printCertificate = () => {
  console.log('Print certificate for student:', studentData.id)
  // Implement print logic
}

const deleteRecord = () => {
  if (confirm('Are you sure you want to delete this student record?')) {
    console.log('Delete student:', studentData.id)
    // Implement delete logic
  }
}

// Address API functions
const fetchDivisions = async () => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const response = await fetch(`${API_BASE_URL}/api/admin/madrasha/divisions/`)
    if (!response.ok) return []
    const data = await response.json()
    return (data.results || []).map(item => ({ id: String(item.did), Division: item.division }))
  } catch (error) {
    console.error('Error fetching divisions:', error)
    return []
  }
}

const fetchDistricts = async (divisionId) => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const url = divisionId ? `${API_BASE_URL}/api/admin/madrasha/districts/?did=${divisionId}` : `${API_BASE_URL}/api/admin/madrasha/districts/`
    const response = await fetch(url)
    if (!response.ok) return []
    const data = await response.json()
    return (data.results || []).map(item => ({ DesID: String(item.desid), District: item.district }))
  } catch (error) {
    console.error('Error fetching districts:', error)
    return []
  }
}

const fetchThanas = async (districtId) => {
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    const url = districtId ? `${API_BASE_URL}/api/admin/madrasha/thanas/?district_id=${districtId}` : `${API_BASE_URL}/api/admin/madrasha/thanas/`
    const response = await fetch(url)
    if (!response.ok) return []
    const data = await response.json()
    return (data.results || []).map(item => ({ Thana_ID: String(item.thana_id), Thana: item.thana }))
  } catch (error) {
    console.error('Error fetching thanas:', error)
    return []
  }
}

// Address event handlers
const handleDivisionChange = async () => {
  try {
    localAddress.district = ''
    localAddress.Thana = ''
    districts.value = []
    thanas.value = []
    if (!localAddress.division) return
    districts.value = await fetchDistricts(localAddress.division)
    // Update address data
    studentAddressData.division = localAddress.division
    studentAddressData.district = ''
    studentAddressData.thana = ''
  } catch (error) {
    console.error('Error loading districts:', error)
  }
}

const handleDistrictChange = async () => {
  try {
    localAddress.Thana = ''
    thanas.value = []
    if (!localAddress.district) return
    thanas.value = await fetchThanas(localAddress.district)
    // Update address data
    studentAddressData.district = localAddress.district
    studentAddressData.thana = ''
  } catch (error) {
    console.error('Error loading thanas:', error)
  }
}

const handleThanaChange = () => {
  // Update address data
  studentAddressData.thana = localAddress.Thana
}

// Address dropdown change handlers
const onDivisionChange = (event) => {
  handleDivisionChange()
}

const onDistrictChange = (event) => {
  handleDistrictChange()
}

const onThanaChange = (event) => {
  handleThanaChange()
}

// Fetch combined student data from API
const fetchStudentData = async (studentId) => {
  try {
    loading.value = true
    error.value = null

    // Get user ID from localStorage or wherever it's stored
    const userId = localStorage.getItem('user_id') || null
    const params = { user_id: userId }

    // Fetch combined student data using the StudentService
    const data = await StudentService.getStudent(studentId, params)

    // Update student data with all fields from the first table
    Object.assign(studentData, {
      id: data.id,
      photo: data.photo,
      student_name_bn: data.student_name_bn,
      student_name_ar: data.student_name_ar,
      student_name_en: data.student_name_en,
      father_name_bn: data.father_name_bn,
      father_name_ar: data.father_name_ar,
      father_name_en: data.father_name_en,
      mother_name_bn: data.mother_name_bn,
      mother_name_ar: data.mother_name_ar,
      mother_name_en: data.mother_name_en,
      roll_no: data.roll_no,
      reg_no: data.reg_no,
      year: data.year,
      date_of_birth: data.date_of_birth,
      mobile: data.mobile,
      status: data.status,
      ip_address: data.ip_address,
      created_at: data.created_at,
      updated_at: data.updated_at,
      marhala_id: data.marhala_id,
      cid: data.cid,
      srtype: data.srtype,
      hijri_year: data.hijri_year,
      bangla_year: data.bangla_year,
      students_type: data.students_type,
      exam_id: data.exam_id,
      madrasha_id: data.madrasha_id,
      markaz_id: data.markaz_id,
      is_old: data.is_old,
      irregular_sub: data.irregular_sub,
      // Include mapped fields for display
      current_class: data.current_class,
      current_madrasha: data.current_madrasha,
      current_markaz: data.current_markaz,
      exam_name_Bn: data.exam_name_Bn,
      student_type: data.student_type
    })

    // Update address data with fields from the second table
    Object.assign(studentAddressData, {
      division: data.division,
      district: data.district,
      thana: data.thana,
      post_office: data.post_office,
      passport_photo: data.passport_photo,
      birth_certificate_no: data.birth_certificate_no,
      birth_certificate_photo: data.birth_certificate_photo,
      nid_no: data.nid_no,
      nid_photo: data.nid_photo
    })

    // Initialize local address state with current address data
    localAddress.division = data.division || ''
    localAddress.district = data.district || ''
    localAddress.Thana = data.thana || ''
  } catch (err) {
    console.error('Error fetching student data:', err)
    error.value = err.message || 'Failed to fetch student data'
  } finally {
    loading.value = false
  }
}

// Lifecycle hook
onMounted(async () => {
  const studentId = route.params.id
  if (studentId) {
    await fetchStudentData(studentId)

    // Load divisions data for address dropdowns
    divisions.value = await fetchDivisions()

    // If student has division selected, load corresponding districts
    if (localAddress.division) {
      districts.value = await fetchDistricts(localAddress.division)
    }

    // If student has district selected, load corresponding thanas
    if (localAddress.district) {
      thanas.value = await fetchThanas(localAddress.district)
    }
  } else {
    error.value = 'No student ID provided'
    loading.value = false
  }
})
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Ensure proper z-index for dropdown visibility */
:deep(.p-dropdown-list) {
  z-index: 1000 !important;
}

/* Container overflow fixes for dropdown visibility */
.overflow-visible {
  overflow: visible !important;
}
</style>
