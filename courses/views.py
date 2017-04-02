from django.shortcuts import render, redirect
from courses.models import Course
from courses.forms import CourseModelForm, LessonModelForm
from django.contrib import messages


# Create your views here.
def detail(request, id):
    course = Course.objects.get(pk=id)
    lessons = course.lesson_set.all()
    return render(request, 'courses/detail.html', {
                  'course': course,
                  'lessons': lessons,
                  'coach': course.coach,
                  'assistant': course.assistant, })


def add(request):
    if request.method == "POST":
        form = CourseModelForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, "Course {} has been successfully added.".format(course.name))
            return redirect('/')
    else:
        form = CourseModelForm()
    return render(request, 'courses/add.html', {'form': form})


def edit(request, id):
    course = Course.objects.get(pk=id)
    if request.method == "POST":
        form = CourseModelForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, "The changes have been saved.")
            return redirect('courses:edit', id)
    form = CourseModelForm(instance=course)
    return render(request, 'courses/edit.html', {'form': form})

def remove(request, id):
        course = Course.objects.get(pk=id)
        if request.method == "POST":
            course.delete()
            messages.success(request, "Course {} has been deleted.".format(course.name))
            return redirect('/')
        return render(request, 'courses/remove.html', {'course': course})
    
def add_lesson(request):
    if request.method == "POST":
        form = LessonModelForm(request.POST)
        if form.is_valid():
            lesson = form.save()
            #print("======>>>>>>\t",lesson,lesson.course_id)
            messages.success(request, "Lesson {} has been successfully added.".format(lesson.subject))
            return redirect('courses:detail', lesson.course_id)
    else:
        form = LessonModelForm()#initial={'course':lesson.course_id})
    return render(request, 'courses/add_lesson.html', {'form': form})
    