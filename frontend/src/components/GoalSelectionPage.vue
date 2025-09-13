<!-- GoalSelectionPage.vue -->
<template>
  <div class="goal-selection-page">
    <div class="mb-12 text-center">
      <h1 class="text-5xl font-black text-[#5a4633] uppercase tracking-[-2px] mb-2 max-md:text-[2rem]">
        Select Goal
      </h1>
      <p class="text-[1.2rem] text-[#64748b] font-medium uppercase tracking-[1px]">
        To Start Your Journey
      </p>
    </div>

    <div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-8 mt-8 max-md:grid-cols-[1fr]">
      <div
        v-for="goal in goals"
        :key="goal.id"
        class="cursor-pointer relative bg-[#FFF] shadow-[0_10px_30px_rgba(0,0,0,0.1)] text-center overflow-hidden p-8 rounded-[20px] transition-all duration-300 ease-in-out before:content-[''] before:absolute before:h-1.5 before:rounded-[20px_20px_0_0] before:top-0 before:inset-x-0 hover:translate-y-[-5px] hover:shadow-[0_20px_40px_rgba(0,0,0,0.15)]"
        :class="{
          'before:bg-[#B8D7DF]': goal.type === 'fitness',
          'before:bg-[#EDB6B6]': goal.type === 'nutrition',
          'before:bg-[#DED8B4]': goal.type === 'wellness',
        }"
        @click="selectGoal(goal)"
      >
        <div
          class="w-[80px] h-[80px] flex items-center justify-center text-[2rem] text-[#FFF] font-[bold] mt-0 mb-6 mx-auto rounded-[50%]"
          :class="{
            'bg-[linear-gradient(135deg,#B8D7DF)]': goal.type === 'fitness',
            'bg-[linear-gradient(135deg,#EDB6B6)]': goal.type === 'nutrition',
            'bg-[linear-gradient(135deg,#DED8B4)]': goal.type === 'wellness',
          }">
          {{ goal.icon }}
        </div>

        <h3 class="text-2xl font-extrabold text-[#1e293b] uppercase tracking-[-1px] mb-4">
          {{ goal.title }}
        </h3>
        <p class="text-[#64748b] leading-normal mb-6">
          {{ goal.description }}
        </p>

        <div class="flex justify-center gap-3 flex-wrap mb-6">
          <span
            v-for="feature in goal.features"
            :key="feature"
            class="text-[#475569] bg-[#f1f5f9] text-[0.8rem] font-semibold px-3 py-1 rounded-[15px]"
          >
            {{ feature }}
          </span>
        </div>

        <div class="text-left mb-8">
          <div
            v-for="detail in goal.details"
            :key="detail"
            class="flex items-center text-[#64748b] text-[0.9rem] mb-2 before:content-['•'] before:text-[#10b981] before:font-[bold] before:w-[1em] before:mr-2"
          >
            {{ detail }}
          </div>
        </div>

        <button class="text-[#FFF] bg-[#609da1] font-semibold cursor-pointer transition-transform duration-[0.2s] ease-[ease] w-full text-base px-8 py-3 rounded-[25px] border-[none] hover:translate-y-[-2px]">Click to Select</button>
      </div>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="fixed flex items-center justify-center bg-[rgba(0,0,0,0.8)] z-[1000] inset-0 animate-fadeIn" @click="closeModal">
      <div class="bg-[#FFF] text-center max-w-[400px] w-[90%] p-8 rounded-[20px] animate-slideUp max-md:w-[calc(100%_-_2rem)] max-md:m-4" @click.stop>
        <div class="text-5xl mb-4">✨</div>
        <h2 class="text-[#1e293b] font-bold mb-4">Goal Selected!</h2>
        <p class="text-[#6b7280] mb-2">You selected: <strong>{{ selectedGoal?.title }}</strong></p>
        <p class="text-[#10b981] font-semibold mx-0 my-4">Redirecting to dashboard...</p>
        <div class="h-1.5 bg-[#e5e7eb] overflow-hidden mt-4 rounded-[3px]">
          <div class="h-full bg-[linear-gradient(90deg,#10b981,#059669)] transition-[width] duration-300 ease-[ease] rounded-[3px]" :style="{ width: progressWidth + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'GoalSelectionPage',
  emits: ['goal-selected'],
  setup(props, { emit }) {
    const selectedGoal = ref(null)
    const showSuccessModal = ref(false)
    const progressWidth = ref(0)

    const goals = ref([
      {
        id: 'fitness',
        type: 'fitness',
        icon: '🏃‍♂️',
        title: 'Fitness Journey',
        description: 'Build strength, boost cardio, and feel athletic again.',
        features: ['8 weeks', 'Strength + Cardio', 'Beginner'],
        details: [
          '3-day split plan',
          'Video-guided moves',
          'Weekly progress check'
        ]
      },
      {
        id: 'nutrition',
        type: 'nutrition',
        icon: '🥗',
        title: 'Nutrition Focus',
        description: 'Clean eating plan with macro guidance and easy recipes.',
        features: ['6 weeks', 'Balanced macros', 'All levels'],
        details: [
          'Personalized portions',
          'Grocery list',
          'Thai-friendly recipes'
        ]
      },
      {
        id: 'wellness',
        type: 'wellness',
        icon: '🧘‍♀️',
        title: 'Wellness Balance',
        description: 'Mindfulness, mobility, and light movement for balance.',
        features: ['4 weeks', 'Mind & Body', 'Gentle'],
        details: [
          '10-min daily flow',
          'Breathwork guides',
          'Sleep routine'
        ]
      }
    ])

    const selectGoal = (goal) => {
      selectedGoal.value = goal
      showSuccessModal.value = true

      // Animate progress bar
      let progress = 0
      const interval = setInterval(() => {
        progress += 2
        progressWidth.value = progress

        if (progress >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            emit('goal-selected', goal)
            closeModal()
          }, 500)
        }
      }, 30)
    }

    const closeModal = () => {
      showSuccessModal.value = false
      progressWidth.value = 0
    }

    return {
      goals,
      selectedGoal,
      showSuccessModal,
      progressWidth,
      selectGoal,
      closeModal
    }
  }
}
</script>
